from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.api.serializers import UserSerializer
from accounts.api.admin_serializers import AdminActionSerializer
from accounts.models import User
from accounts.permissions import IsAdministrator
from accounts.services import anonymize_user
from audit.services import record_audit_event


class AdminUserListView(generics.ListAPIView):
    queryset = User.objects.all().prefetch_related("user_roles__role")
    serializer_class = UserSerializer
    permission_classes = [IsAdministrator]
    search_fields = ["email", "first_name", "last_name", "phone_number"]
    ordering_fields = ["created_at", "email", "is_active"]


class AdminUserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all().prefetch_related("user_roles__role")
    serializer_class = UserSerializer
    permission_classes = [IsAdministrator]


class AdminUserSuspendView(generics.GenericAPIView):
    serializer_class = AdminActionSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdministrator]

    def post(self, request, pk):
        user = self.get_object()
        was_active = user.is_active
        user.is_active = False
        user.suspended_at = timezone.now()
        user.save(update_fields=["is_active", "suspended_at", "updated_at"])
        record_audit_event(actor=request.user, action="USER_SUSPENDED", target=user, before={"is_active": was_active}, after={"is_active": False}, reason=request.data.get("reason", ""))
        return Response({"status": "suspended"})


class AdminUserReactivateView(generics.GenericAPIView):
    serializer_class = AdminActionSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdministrator]

    def post(self, request, pk):
        user = self.get_object()
        was_active = user.is_active
        user.is_active = True
        user.suspended_at = None
        user.save(update_fields=["is_active", "suspended_at", "updated_at"])
        record_audit_event(actor=request.user, action="USER_REACTIVATED", target=user, before={"is_active": was_active}, after={"is_active": True}, reason=request.data.get("reason", ""))
        return Response({"status": "active"})


class AdminUserDeleteView(generics.DestroyAPIView):
    serializer_class = AdminActionSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdministrator]

    def perform_destroy(self, instance):
        before = {"is_active": instance.is_active, "email": instance.email}
        anonymize_user(instance)
        record_audit_event(actor=self.request.user, action="USER_DELETED", target=instance, before=before, after={"is_active": False}, reason=self.request.data.get("reason", ""))
