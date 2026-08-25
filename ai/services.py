import hashlib
import json
import logging
import time

from ai.models import AIFeatureConfig, AIInteraction, AIInteractionStatus, HumanReviewStatus

logger = logging.getLogger(__name__)

NON_DIAGNOSTIC_DISCLAIMER = "This is AI-assisted decision support, not a diagnosis, prescription, or emergency substitute. Consult a qualified veterinary professional."


class ProviderResult:
    def __init__(self, ok, provider_key, narrative="", metadata=None):
        self.ok = ok
        self.provider_key = provider_key
        self.narrative = narrative
        self.metadata = metadata or {}


class BaseAIProvider:
    provider_key = "base"

    def generate(self, *, feature_key, context, timeout_seconds):
        raise NotImplementedError


class NoopProvider(BaseAIProvider):
    """No outbound call is made. Used when no real provider adapter is configured for this environment."""

    provider_key = "noop"

    def generate(self, *, feature_key, context, timeout_seconds):
        return ProviderResult(False, self.provider_key, metadata={"error": "No AI provider adapter is implemented for this environment."})


class ConsoleProvider(BaseAIProvider):
    """Deterministic, offline stand-in used for local/dev verification. Never calls a third party."""

    provider_key = "console"

    def generate(self, *, feature_key, context, timeout_seconds):
        logger.info("ai.console_provider.generate", extra={"feature_key": feature_key, "context_keys": sorted(context.keys())})
        return ProviderResult(True, self.provider_key, narrative="Automated decision-support narrative is not independently verified. Review the structured result below.", metadata={"context_keys": sorted(context.keys())})


PROVIDER_REGISTRY = {"noop": NoopProvider, "console": ConsoleProvider}


def get_feature_config(feature_key):
    return AIFeatureConfig.objects.filter(feature_key=feature_key).select_related("provider").first()


def redact_context(inputs, allowed_fields):
    """Allowlist-only redaction: only explicitly permitted, non-identifying field names ever leave the process boundary."""
    allowed = set(allowed_fields or [])
    return {key: value for key, value in (inputs or {}).items() if key in allowed}


def hash_payload(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode("utf-8")).hexdigest()


def resolve_provider(provider_config):
    if provider_config is None or not provider_config.is_enabled:
        return NoopProvider()
    provider_cls = PROVIDER_REGISTRY.get(provider_config.provider_key, NoopProvider)
    return provider_cls()


def invoke_ai_feature(*, user, feature_key, full_inputs, deterministic_fn, urgent=False):
    """
    Wraps a local, deterministic engine call (e.g. disease.services.assess_disease) with an optional
    AI narrative layer. The deterministic result is always computed locally and is never sent to any
    provider. Only an allowlisted, redacted subset of `full_inputs` may leave the process boundary.
    Any provider failure, timeout, or missing/disabled configuration falls back to the deterministic
    result unchanged. Every call is recorded in an auditable AIInteraction.
    """
    deterministic_result = deterministic_fn()
    feature = get_feature_config(feature_key)
    redacted = redact_context(full_inputs, feature.allowed_context_fields if feature else [])
    input_hash = hash_payload(redacted)

    if feature is None or not feature.is_enabled:
        interaction = AIInteraction.objects.create(user=user, feature_key=feature_key, input_hash=input_hash, redacted_input=redacted, output=deterministic_result, status=AIInteractionStatus.SUPPRESSED)
        return {**deterministic_result, "ai_narrative": None, "ai_status": interaction.status, "disclaimer": NON_DIAGNOSTIC_DISCLAIMER}

    provider = resolve_provider(feature.provider)
    timeout_seconds = feature.provider.timeout_seconds if feature.provider else 8
    started = time.monotonic()
    try:
        result = provider.generate(feature_key=feature_key, context=redacted, timeout_seconds=timeout_seconds)
    except Exception:
        logger.exception("ai.provider.generate_failed", extra={"feature_key": feature_key, "provider_key": provider.provider_key})
        result = ProviderResult(False, provider.provider_key, metadata={"error": "Provider call raised an exception."})
    latency_ms = int((time.monotonic() - started) * 1000)

    status = AIInteractionStatus.COMPLETED if result.ok else AIInteractionStatus.FALLBACK
    output = {**deterministic_result, "ai_narrative": result.narrative if result.ok else None}
    human_review_status = HumanReviewStatus.NOT_REQUIRED
    if urgent and feature.requires_human_review_on_urgent:
        human_review_status = HumanReviewStatus.PENDING

    interaction = AIInteraction.objects.create(
        user=user,
        feature_key=feature_key,
        provider_key=provider.provider_key,
        model_version=feature.provider.model_version if feature.provider else "",
        input_hash=input_hash,
        redacted_input=redacted,
        output=output,
        status=status,
        latency_ms=latency_ms,
        human_review_status=human_review_status,
    )
    return {**deterministic_result, "ai_narrative": output["ai_narrative"], "ai_status": interaction.status, "human_review_status": interaction.human_review_status, "disclaimer": NON_DIAGNOSTIC_DISCLAIMER}
