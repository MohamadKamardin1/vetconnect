from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from accounts.permissions import IsAdministrator
from discovery.api.serializers import PublicReviewSerializer, ReviewCreateSerializer, ServiceSerializer
from discovery.api.admin_serializers import ModerationActionSerializer
from discovery.models import ModerationStatus, Review, Service
from professionals.models import Clinic, ProfessionalProfile, VerificationStatus


class PublicServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(is_active=True, clinic__verification_status=VerificationStatus.VERIFIED, clinic__is_active=True).select_related("clinic", "professional")
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    filterset_fields = ["category", "clinic", "professional"]
    search_fields = ["name", "category", "description", "clinic__name"]


class PublicReviewListView(generics.ListAPIView):
    serializer_class = PublicReviewSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Review.objects.filter(moderation_status=ModerationStatus.APPROVED).filter(Q(clinic__verification_status=VerificationStatus.VERIFIED) | Q(professional__verification_status=VerificationStatus.VERIFIED)).select_related("author")


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        clinic = serializer.validated_data.get("clinic")
        professional = serializer.validated_data.get("professional")
        if clinic and clinic.owner_id == self.request.user.pk:
            raise serializers.ValidationError("You cannot review your own clinic.")
        if professional and professional.user_id == self.request.user.pk:
            raise serializers.ValidationError("You cannot review yourself.")
        serializer.save()


class ReviewModerationView(generics.GenericAPIView):
    serializer_class = ModerationActionSerializer
    permission_classes = [IsAdministrator]

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        action = self.get_serializer(data=request.data)
        action.is_valid(raise_exception=True)
        decision = action.validated_data["moderation_status"]
        if decision not in {ModerationStatus.APPROVED, ModerationStatus.REJECTED, ModerationStatus.HIDDEN}:
            return Response({"error": {"code": "invalid_moderation_status", "message": "Unsupported moderation status."}}, status=status.HTTP_400_BAD_REQUEST)
        review.moderation_status = decision
        review.moderation_reason = action.validated_data.get("moderation_reason", "")
        review.save(update_fields=["moderation_status", "moderation_reason", "updated_at"])
        return Response({"status": decision.lower()})
