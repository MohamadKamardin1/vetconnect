import pytest
from rest_framework.test import APIClient
from accounts.models import User
from community.models import Post, PublicationStatus, Report, UserBlock


@pytest.mark.django_db
def test_public_feed_only_exposes_published_posts():
    author = User.objects.create_user(email="author@example.com", password="StrongPass123!")
    Post.objects.create(author=author, title="Draft", body="Private", publication_status=PublicationStatus.DRAFT)
    Post.objects.create(author=author, title="Published", body="Public", publication_status=PublicationStatus.PUBLISHED)
    response = APIClient().get("/api/v1/community/posts/")
    assert response.status_code == 200
    assert [item["title"] for item in response.data["results"]] == ["Published"]


@pytest.mark.django_db
def test_self_report_and_self_block_are_denied():
    author = User.objects.create_user(email="author2@example.com", password="StrongPass123!")
    post = Post.objects.create(author=author, title="Post", body="Body", publication_status=PublicationStatus.PUBLISHED)
    client = APIClient()
    client.force_authenticate(user=author)
    report = client.post("/api/v1/community/reports/", {"post": str(post.pk), "reason": "spam"}, format="json")
    block = client.post("/api/v1/community/blocks/create/", {"blocked": str(author.pk)}, format="json")
    assert report.status_code == 400
    assert block.status_code == 400
    assert Report.objects.count() == 0
    assert UserBlock.objects.count() == 0
