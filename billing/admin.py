from django.contrib import admin
from billing.models import BadgePlan, BadgeSubscription, PaymentTransaction, PaymentWebhookEvent


@admin.register(BadgePlan)
class BadgePlanAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "price_tzs", "duration_days", "is_active")
    list_filter = ("code", "is_active")
    search_fields = ("name", "code")


@admin.register(BadgeSubscription)
class BadgeSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("professional", "plan", "status", "starts_at", "ends_at", "auto_renew_requested")
    list_filter = ("status", "plan__code", "auto_renew_requested")
    search_fields = ("professional__user__email", "professional__registration_number")
    readonly_fields = ("created_at", "updated_at")


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("client_reference", "payer", "amount_tzs", "currency", "status", "channel", "created_at", "paid_at")
    list_filter = ("provider", "status", "channel", "currency")
    search_fields = ("client_reference", "provider_order_reference", "provider_payment_reference", "payer__email")
    readonly_fields = ("request_payload", "response_payload", "created_at", "updated_at", "paid_at")


@admin.register(PaymentWebhookEvent)
class PaymentWebhookEventAdmin(admin.ModelAdmin):
    list_display = ("provider_event_id", "event_name", "order_reference", "checksum_valid", "received_at", "processed_at")
    list_filter = ("provider", "event_name", "checksum_valid")
    search_fields = ("provider_event_id", "order_reference")
    readonly_fields = ("payload", "received_at", "processed_at")
