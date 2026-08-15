from rest_framework import serializers
from community.models import Post, Report, UserBlock


class PublicPostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.display_name", read_only=True)

    class Meta:
        model = Post
        fields = ["id", "author", "author_name", "title", "body", "published_at", "created_at"]
        read_only_fields = fields


class PostWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "body", "publication_status"]

    def validate_publication_status(self, value):
        if value not in {"DRAFT", "PENDING_REVIEW"}:
            raise serializers.ValidationError("Authors may save drafts or submit posts for review.")
        return value


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "post", "reporter", "reason", "details", "status", "created_at"]
        read_only_fields = ["id", "reporter", "status", "created_at"]


class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBlock
        fields = ["id", "blocked", "created_at"]
        read_only_fields = ["id", "created_at"]
