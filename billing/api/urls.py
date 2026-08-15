from django.urls import path
from billing.api.views import BadgePaymentCreateView, BadgePaymentListView, BadgePlanListView, BadgeSubscriptionListView, ClickPesaWebhookView

urlpatterns = [
    path("badge-plans/", BadgePlanListView.as_view(), name="badge-plan-list"),
    path("badge-subscriptions/", BadgeSubscriptionListView.as_view(), name="badge-subscription-list"),
    path("badge-payments/", BadgePaymentCreateView.as_view(), name="badge-payment-create"),
    path("badge-payments/history/", BadgePaymentListView.as_view(), name="badge-payment-history"),
    path("webhooks/clickpesa/", ClickPesaWebhookView.as_view(), name="clickpesa-webhook"),
]
