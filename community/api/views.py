from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from accounts.permissions import IsAdministrator
from community.api.serializers import PostWriteSerializer, PublicPostSerializer, ReportSerializer, UserBlockSerializer
from community.api.admin_serializers import ReportModerationSerializer
from community.models import Post, PublicationStatus, Report, UserBlock


class PublicPostListView(generics.ListAPIView):
    serializer_class = PublicPostSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Post.objects.filter(publication_status=PublicationStatus.PUBLISHED).select_related("author")


class MyPostListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return PostWriteSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)

    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        if post.publication_status == PublicationStatus.PENDING_REVIEW:
            post.publication_status = PublicationStatus.PUBLISHED
            post.published_at = timezone.now()
            post.save(update_fields=["publication_status", "published_at"])


class MyPostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostWriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Post.objects.none()
        return Post.objects.filter(author=self.request.user)


class ReportCreateView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.request.data.get("post"))
        if post.author_id == self.request.user.pk:
            raise serializers.ValidationError("You cannot report your own post.")
        serializer.save(reporter=self.request.user, post=post)


class ReportListView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAdministrator]
    queryset = Report.objects.select_related("post", "reporter").all()


class UserBlockCreateView(generics.CreateAPIView):
    serializer_class = UserBlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        blocked = serializer.validated_data["blocked"]
        if blocked == self.request.user:
            raise serializers.ValidationError("You cannot block yourself.")
        serializer.save(blocker=self.request.user)


class UserBlockListView(generics.ListAPIView):
    serializer_class = UserBlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return UserBlock.objects.none()
        return UserBlock.objects.filter(blocker=self.request.user).select_related("blocked")


class ReportModerationView(generics.GenericAPIView):
    permission_classes = [IsAdministrator]
    serializer_class = ReportModerationSerializer
    queryset = Report.objects.all()

    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        decision = request.data.get("status")
        if decision not in {Report.Status.REVIEWED, Report.Status.DISMISSED}:
            return Response({"error": {"code": "invalid_report_status", "message": "Unsupported report status."}}, status=status.HTTP_400_BAD_REQUEST)
        report.status = decision
        report.save(update_fields=["status"])
        return Response({"status": decision})
