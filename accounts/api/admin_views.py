from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from accounts.api.serializers import UserSerializer
from accounts.api.admin_serializers import AdminActionSerializer
from accounts.models import User
from accounts.permissions import IsAdministrator


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
        user.is_active = False
        user.suspended_at = timezone.now()
        user.save(update_fields=["is_active", "suspended_at", "updated_at"])
        return Response({"status": "suspended"})


class AdminUserReactivateView(generics.GenericAPIView):
    serializer_class = AdminActionSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdministrator]

    def post(self, request, pk):
        user = self.get_object()
        user.is_active = True
        user.suspended_at = None
        user.save(update_fields=["is_active", "suspended_at", "updated_at"])
        return Response({"status": "active"})


class AdminUserDeleteView(generics.DestroyAPIView):
    serializer_class = AdminActionSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdministrator]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.email = f"deleted+{instance.pk}@invalid.local"
        instance.phone_number = None
        instance.first_name = "Deleted"
        instance.last_name = "User"
        instance.set_unusable_password()
        instance.save(update_fields=["is_active", "email", "phone_number", "first_name", "last_name", "password", "updated_at"])
