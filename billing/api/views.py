from django.db.models import Prefetch
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from billing.api.serializers import BadgePaymentCreateSerializer, BadgePlanSerializer, BadgeSubscriptionSerializer, ClickPesaWebhookSerializer, PaymentTransactionSerializer
from billing.models import BadgePlan, BadgeSubscription, PaymentTransaction
from billing.services import create_badge_payment, reconcile_clickpesa_webhook
from billing.tasks import initiate_clickpesa_payment_task


class BadgePlanListView(generics.ListAPIView):
    queryset = BadgePlan.objects.filter(is_active=True)
    serializer_class = BadgePlanSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class BadgeSubscriptionListView(generics.ListAPIView):
    serializer_class = BadgeSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return BadgeSubscription.objects.none()
        return BadgeSubscription.objects.filter(professional__user=self.request.user).select_related("plan", "professional")


class BadgePaymentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=BadgePaymentCreateSerializer, responses={202: PaymentTransactionSerializer})
    def post(self, request):
        serializer = BadgePaymentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        professional = getattr(request.user, "professional_profile", None)
        if professional is None:
            return Response({"error": {"code": "professional_profile_required", "message": "Only veterinarian professional profiles may purchase a verification badge."}}, status=status.HTTP_403_FORBIDDEN)
        try:
            payment = create_badge_payment(professional=professional, plan=serializer.validated_data["plan"], phone_number=serializer.validated_data["phone_number"])
        except ValueError as exc:
            return Response({"error": {"code": "badge_payment_not_allowed", "message": str(exc)}}, status=status.HTTP_400_BAD_REQUEST)
        initiate_clickpesa_payment_task.delay(str(payment.id))
        return Response(PaymentTransactionSerializer(payment).data, status=status.HTTP_202_ACCEPTED)


class BadgePaymentListView(generics.ListAPIView):
    serializer_class = PaymentTransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return PaymentTransaction.objects.none()
        return PaymentTransaction.objects.filter(payer=self.request.user).select_related("subscription__plan")


class ClickPesaWebhookView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    @extend_schema(request=ClickPesaWebhookSerializer, responses={200: dict})
    def post(self, request):
        checksum = request.headers.get("X-ClickPesa-Checksum") or request.data.get("checksum", "")
        try:
            _, created = reconcile_clickpesa_webhook(payload=request.data, received_checksum=checksum)
        except ValueError as exc:
            return Response({"error": {"code": "invalid_webhook", "message": str(exc)}}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"accepted": True, "duplicate": not created}, status=status.HTTP_200_OK)
