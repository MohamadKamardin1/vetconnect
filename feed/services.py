from decimal import Decimal
from feed.models import FeedRule


def calculate_feed(*, species_code, production_category, inputs):
    required = {"animal_count", "average_weight_kg", "feed_type"}
    missing = sorted(required - set(inputs))
    if missing:
        return None, {"status": "INVALID", "missing_inputs": missing, "message": "Required metric inputs are missing."}
    try:
        count = Decimal(str(inputs["animal_count"]))
        weight = Decimal(str(inputs["average_weight_kg"]))
    except Exception:
        return None, {"status": "INVALID", "message": "animal_count and average_weight_kg must be numeric."}
    if count <= 0 or weight <= 0:
        return None, {"status": "INVALID", "message": "animal_count and average_weight_kg must be positive."}
    rule = FeedRule.objects.filter(species_code=species_code, production_category=production_category, is_active=True).order_by("-version").first()
    if not rule:
        return None, {"status": "MISSING_CONFIGURATION", "message": "No verified feed rule is configured for this species and category."}
    if rule.formula_key != "body_weight_ratio":
        return rule, {"status": "MISSING_CONFIGURATION", "message": "The configured formula is not enabled in this deployment."}
    ratio = Decimal(str(rule.assumptions.get("daily_ratio", "0")))
    if ratio <= 0:
        return rule, {"status": "MISSING_CONFIGURATION", "message": "The feed rule is missing a positive daily ratio."}
    daily_kg = count * weight * ratio
    return rule, {"status": "COMPLETED", "daily_feed_kg": str(daily_kg.quantize(Decimal("0.001"))), "assumptions": rule.assumptions, "version": rule.version}
