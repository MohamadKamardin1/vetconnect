from django.contrib import admin
from ai.models import AIFeatureConfig, AIInteraction, AIProviderConfig


@admin.register(AIProviderConfig)
class AIProviderConfigAdmin(admin.ModelAdmin):
    list_display = ("provider_key", "display_name", "model_name", "model_version", "is_enabled", "timeout_seconds")
    list_filter = ("is_enabled",)
    search_fields = ("provider_key", "display_name")


@admin.register(AIFeatureConfig)
class AIFeatureConfigAdmin(admin.ModelAdmin):
    list_display = ("feature_key", "is_enabled", "requires_human_review_on_urgent", "provider")
    list_filter = ("is_enabled", "provider")
    search_fields = ("feature_key",)


@admin.register(AIInteraction)
class AIInteractionAdmin(admin.ModelAdmin):
    list_display = ("feature_key", "user", "provider_key", "status", "human_review_status", "latency_ms", "created_at")
    list_filter = ("feature_key", "status", "human_review_status", "provider_key")
    search_fields = ("user__email", "input_hash")
    readonly_fields = ("redacted_input", "output", "input_hash", "created_at")
