from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from audit.services import record_audit_event
from privacy.api.serializers import DataDeletionRequestCreateSerializer, DataDeletionRequestSerializer, DataExportRequestSerializer
from privacy.models import DataDeletionRequest, DataExportRequest
from privacy.services import confirm_deletion, run_export


class DataExportRequestListCreateView(generics.ListCreateAPIView):
    """Self-service data export: a user may request and read only their own export requests."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DataExportRequestSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return DataExportRequest.objects.none()
        return DataExportRequest.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        export_request = DataExportRequest.objects.create(user=request.user)
        run_export(export_request)
        record_audit_event(actor=request.user, action="DATA_EXPORT_COMPLETED", target=export_request, reason="Self-service export request")
        return Response(self.get_serializer(export_request).data, status=status.HTTP_201_CREATED)


class DataDeletionRequestListCreateView(generics.ListCreateAPIView):
    """Self-service account deletion, step 1: create a pending request. Nothing is deleted until confirm/."""

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return DataDeletionRequest.objects.none()
        return DataDeletionRequest.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        return DataDeletionRequestCreateSerializer if self.request.method == "POST" else DataDeletionRequestSerializer

    def create(self, request, *args, **kwargs):
        request_serializer = DataDeletionRequestCreateSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        deletion_request = DataDeletionRequest.objects.create(user=request.user, reason=request_serializer.validated_data["reason"])
        record_audit_event(actor=request.user, action="DATA_DELETION_REQUESTED", target=deletion_request, reason=deletion_request.reason)
        return Response(DataDeletionRequestSerializer(deletion_request).data, status=status.HTTP_201_CREATED)


class DataDeletionConfirmView(APIView):
    """Self-service account deletion, step 2: confirm the most recent pending request and execute it."""

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(request=None, responses={200: DataDeletionRequestSerializer, 400: OpenApiTypes.OBJECT})
    def post(self, request):
        deletion_request = DataDeletionRequest.objects.filter(user=request.user, status=DataDeletionRequest.Status.PENDING).order_by("-requested_at").first()
        if deletion_request is None:
            return Response({"error": {"code": "no_pending_deletion_request", "message": "No pending deletion request found. Create one first."}}, status=status.HTTP_400_BAD_REQUEST)
        confirm_deletion(deletion_request)
        record_audit_event(actor=request.user, action="DATA_DELETION_COMPLETED", target=deletion_request, reason=deletion_request.reason)
        return Response(DataDeletionRequestSerializer(deletion_request).data)
