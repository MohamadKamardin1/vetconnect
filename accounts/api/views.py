from django.contrib.auth import update_session_auth_hash
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from accounts.api.serializers import EmailVerificationResendSerializer, EmailVerificationSerializer, LoginSerializer, PasswordChangeSerializer, RegistrationSerializer, UserSerializer
from accounts.models import User
from accounts.services import EmailVerificationDeliveryError, EmailVerificationError, EmailVerificationRateLimited, issue_email_verification_code, verify_email_code


class EmailVerificationThrottle(AnonRateThrottle):
    scope = "email_verification"


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = RegistrationSerializer

    @extend_schema(request=RegistrationSerializer, responses={201: dict, 503: dict})
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        try:
            issue_email_verification_code(user)
        except EmailVerificationDeliveryError:
            return Response(
                {"error": {"code": "verification_delivery_failed", "message": "We could not send a verification code. Please try again shortly."}},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        return Response(
            {"status": "verification_pending", "email": user.email, "expires_in_minutes": 10},
            status=status.HTTP_201_CREATED,
        )


class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [EmailVerificationThrottle]
    serializer_class = EmailVerificationSerializer

    @extend_schema(request=EmailVerificationSerializer, responses={200: dict, 400: dict})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = verify_email_code(**serializer.validated_data)
        except EmailVerificationError:
            return Response(
                {"error": {"code": "invalid_verification_code", "message": "That code is invalid or has expired. Request a new code and try again."}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh), "user": UserSerializer(user).data})


class ResendEmailVerificationView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    throttle_classes = [EmailVerificationThrottle]
    serializer_class = EmailVerificationResendSerializer

    @extend_schema(request=EmailVerificationResendSerializer, responses={200: dict})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(email__iexact=serializer.validated_data["email"], is_active=False, email_verified_at__isnull=True).first()
        if not user:
            return Response({"status": "verification_pending", "message": "If an account is awaiting verification, a code will be sent shortly."})
        try:
            issue_email_verification_code(user)
        except EmailVerificationRateLimited as exc:
            return Response({"status": "verification_pending", "retry_after_seconds": exc.retry_after_seconds})
        except EmailVerificationDeliveryError:
            return Response({"status": "verification_pending", "message": "We could not send a new code just yet. Please try again shortly."})
        return Response({"status": "verification_pending", "expires_in_minutes": 10})


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    serializer_class = LoginSerializer

    @extend_schema(request=LoginSerializer, responses={200: dict})
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh), "user": UserSerializer(user).data})


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class PasswordChangeView(generics.GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.validated_data["old_password"]):
            return Response({"error": {"code": "invalid_credentials", "message": "Current password is incorrect."}}, status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save(update_fields=["password", "updated_at"])
        update_session_auth_hash(request, request.user)
        return Response({"status": "password_changed"})
