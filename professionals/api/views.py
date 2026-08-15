from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from professionals.api.serializers import ClinicSerializer, CredentialDocumentSerializer, ProfessionalCreateSerializer, ProfessionalPublicSerializer
from professionals.api.admin_serializers import KYCActionSerializer
from professionals.models import Clinic, CredentialDocument, KYCReview, ProfessionalProfile, VerificationStatus
from accounts.permissions import IsAdministrator, IsOwnerOrAdministrator


class ProfessionalListView(generics.ListAPIView):
    queryset = ProfessionalProfile.objects.filter(verification_status=VerificationStatus.VERIFIED, is_active=True).select_related("user", "region", "district")
    serializer_class = ProfessionalPublicSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    filterset_fields = ["professional_type", "region__code", "district__code", "is_available"]
    search_fields = ["user__first_name", "user__last_name", "professional_type", "bio"]


class ProfessionalCreateView(generics.CreateAPIView):
    serializer_class = ProfessionalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()


class ProfessionalMeView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfessionalCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProfessionalProfile.objects.filter(user=self.request.user)


class ClinicListCreateView(generics.ListCreateAPIView):
    serializer_class = ClinicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Clinic.objects.none()
        if self.request.user.is_superuser or self.request.user.has_role("ADMINISTRATOR"):
            return Clinic.objects.select_related("owner", "region", "district")
        return Clinic.objects.filter(Q(owner=self.request.user) | Q(staff_members__user=self.request.user, staff_members__is_active=True)).distinct().select_related("owner", "region", "district")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CredentialCreateView(generics.CreateAPIView):
    serializer_class = CredentialDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CredentialListView(generics.ListAPIView):
    serializer_class = CredentialDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return CredentialDocument.objects.none()
        return CredentialDocument.objects.filter(owner=self.request.user)


class KYCReviewView(generics.GenericAPIView):
    serializer_class = KYCActionSerializer
    permission_classes = [IsAdministrator]

    def post(self, request, pk):
        profile = generics.get_object_or_404(ProfessionalProfile, pk=pk)
        action = self.get_serializer(data=request.data)
        action.is_valid(raise_exception=True)
        decision = action.validated_data["decision"]
        if decision not in {VerificationStatus.VERIFIED, VerificationStatus.REJECTED, VerificationStatus.SUSPENDED}:
            return Response({"error": {"code": "invalid_decision", "message": "Unsupported KYC decision."}}, status=status.HTTP_400_BAD_REQUEST)
        KYCReview.objects.create(reviewer=request.user, professional=profile, decision=decision, reason_code=action.validated_data.get("reason_code", ""), notes=action.validated_data.get("notes", ""))
        profile.verification_status = decision
        profile.verified_at = timezone.now() if decision == VerificationStatus.VERIFIED else None
        profile.save(update_fields=["verification_status", "verified_at", "updated_at"])
        return Response({"status": decision.lower()})
