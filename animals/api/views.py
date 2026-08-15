from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.permissions import IsAdministrator
from animals.api.serializers import AnimalSerializer, RecordAccessGrantSerializer, VeterinaryRecordSerializer
from animals.models import Animal, RecordAccessGrant, RecordAccessLog, VeterinaryRecord


def can_read_record(user, record):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.has_role("ADMINISTRATOR"):
        return True
    if record.animal.owner_id == user.pk or record.author_id == user.pk:
        return True
    return RecordAccessGrant.objects.filter(record=record, grantee=user, revoked_at__isnull=True).filter(Q(expires_at__isnull=True) | Q(expires_at__gt=timezone.now())).exists()


class AnimalListCreateView(generics.ListCreateAPIView):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Animal.objects.none()
        return Animal.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AnimalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Animal.objects.filter(owner=self.request.user)


class VeterinaryRecordListCreateView(generics.ListCreateAPIView):
    serializer_class = VeterinaryRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return VeterinaryRecord.objects.none()
        records = VeterinaryRecord.objects.select_related("animal", "author", "clinic", "professional")
        return records.filter(Q(animal__owner=self.request.user) | Q(author=self.request.user) | (Q(access_grants__grantee=self.request.user, access_grants__revoked_at__isnull=True) & (Q(access_grants__expires_at__isnull=True) | Q(access_grants__expires_at__gt=timezone.now())))).distinct()

    def perform_create(self, serializer):
        animal = get_object_or_404(Animal, pk=self.request.data.get("animal"), owner=self.request.user)
        serializer.save(author=self.request.user, animal=animal)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        for item in response.data.get("results", response.data if isinstance(response.data, list) else []):
            try:
                RecordAccessLog.objects.create(record_id=item["id"], actor=request.user, action="LIST")
            except (KeyError, TypeError):
                pass
        return response


class VeterinaryRecordDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = VeterinaryRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return VeterinaryRecord.objects.none()
        return VeterinaryRecord.objects.select_related("animal", "author").filter(Q(animal__owner=self.request.user) | Q(author=self.request.user) | (Q(access_grants__grantee=self.request.user, access_grants__revoked_at__isnull=True) & (Q(access_grants__expires_at__isnull=True) | Q(access_grants__expires_at__gt=timezone.now())))).distinct()

    def retrieve(self, request, *args, **kwargs):
        record = self.get_object()
        RecordAccessLog.objects.create(record=record, actor=request.user, action="READ")
        return Response(self.get_serializer(record).data)


class RecordAccessGrantCreateView(generics.CreateAPIView):
    serializer_class = RecordAccessGrantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        record = get_object_or_404(VeterinaryRecord, pk=self.request.data.get("record"), animal__owner=self.request.user)
        serializer.save(granted_by=self.request.user, record=record)


class RecordAccessGrantListView(generics.ListAPIView):
    serializer_class = RecordAccessGrantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return RecordAccessGrant.objects.none()
        return RecordAccessGrant.objects.filter(Q(granted_by=self.request.user) | Q(grantee=self.request.user)).select_related("record", "granted_by", "grantee")


class RecordAccessGrantRevokeView(generics.GenericAPIView):
    serializer_class = RecordAccessGrantSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        grant = get_object_or_404(RecordAccessGrant, pk=pk, granted_by=request.user, revoked_at__isnull=True)
        grant.revoked_at = timezone.now()
        grant.save(update_fields=["revoked_at"])
        return Response({"status": "revoked"})
