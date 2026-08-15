import pytest
from rest_framework.test import APIClient
from accounts.models import User
from discovery.models import ModerationStatus, Review, Service
from locations.models import District, Region, Territory
from professionals.models import Clinic, ProfessionalProfile, VerificationStatus


@pytest.fixture
def verified_clinic(db):
    owner = User.objects.create_user(email='clinic-discovery@example.tz', password='StrongPassword123!')
    region = Region.objects.create(code='KIL', name='Kilimanjaro', territory=Territory.MAINLAND)
    district = District.objects.create(region=region, code='MOSHI', name='Moshi Urban')
    clinic = Clinic.objects.create(owner=owner, name='Kilimanjaro Vet', registration_number='DISC-CL-1', region=region, district=district, phone_number='+255700000001', address='Moshi', verification_status=VerificationStatus.VERIFIED)
    return owner, clinic


@pytest.mark.django_db
def test_public_services_only_show_verified_clinics(verified_clinic):
    owner, clinic = verified_clinic
    Service.objects.create(clinic=clinic, name='Vaccination', category='PREVENTION', description='Routine vaccination')
    response = APIClient().get('/api/v1/discovery/services/')
    assert response.status_code == 200
    assert response.data['count'] == 1


@pytest.mark.django_db
def test_owner_cannot_self_review_and_approved_reviews_are_public(verified_clinic):
    owner, clinic = verified_clinic
    client = APIClient(); client.force_authenticate(user=owner)
    denied = client.post('/api/v1/discovery/reviews/create/', {'clinic': str(clinic.pk), 'rating': 5, 'body': 'Excellent'}, format='json')
    assert denied.status_code == 400
    reviewer = User.objects.create_user(email='reviewer@example.tz', password='StrongPassword123!')
    review = Review.objects.create(author=reviewer, clinic=clinic, rating=5, body='Excellent', moderation_status=ModerationStatus.APPROVED)
    response = APIClient().get('/api/v1/discovery/reviews/')
    assert response.data['count'] == 1
    assert response.data['results'][0]['id'] == str(review.pk)
