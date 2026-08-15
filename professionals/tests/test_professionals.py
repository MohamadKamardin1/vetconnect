import pytest
from rest_framework.test import APIClient
from accounts.models import User
from locations.models import District, Region, Territory
from professionals.models import Clinic, CredentialDocument, ProfessionalProfile, VerificationStatus


@pytest.fixture
def location_tree(db):
    region = Region.objects.create(code="ARU", name="Arusha", territory=Territory.MAINLAND)
    district = District.objects.create(region=region, code="ARU-URB", name="Arusha Urban")
    return region, district


@pytest.mark.django_db
def test_unverified_professional_is_hidden_from_public_list(location_tree):
    region, district = location_tree
    user = User.objects.create_user(email="vet1@example.tz", password="StrongPassword123!")
    ProfessionalProfile.objects.create(user=user, professional_type="VETERINARIAN", registration_number="VET-001", issuing_body="VCT", region=region, district=district)
    response = APIClient().get("/api/v1/professionals/professionals/")
    assert response.status_code == 200
    assert response.data["count"] == 0


@pytest.mark.django_db
def test_admin_kyc_verification_makes_profile_discoverable(location_tree):
    region, district = location_tree
    admin = User.objects.create_superuser(email="admin2@example.tz", password="StrongPassword123!")
    vet = User.objects.create_user(email="vet2@example.tz", password="StrongPassword123!")
    profile = ProfessionalProfile.objects.create(user=vet, professional_type="VETERINARIAN", registration_number="VET-002", issuing_body="VCT", region=region, district=district)
    client = APIClient()
    client.force_authenticate(user=admin)
    response = client.post(f"/api/v1/professionals/professionals/{profile.pk}/review/", {"decision": "VERIFIED"}, format="json")
    assert response.status_code == 200
    public_response = APIClient().get("/api/v1/professionals/professionals/")
    assert public_response.data["count"] == 1


@pytest.mark.django_db
def test_credential_documents_are_private_and_owner_scoped(location_tree):
    region, district = location_tree
    owner = User.objects.create_user(email="owner-kyc@example.tz", password="StrongPassword123!")
    other = User.objects.create_user(email="other-kyc@example.tz", password="StrongPassword123!")
    profile = ProfessionalProfile.objects.create(user=owner, professional_type="VETERINARIAN", registration_number="VET-003", issuing_body="VCT", region=region, district=district)
    CredentialDocument.objects.create(owner=owner, professional=profile, document_type="LICENSE", object_key="private/key", sha256="a" * 64, mime_type="application/pdf")
    client = APIClient()
    client.force_authenticate(user=other)
    response = client.get("/api/v1/professionals/credentials/")
    assert response.status_code == 200
    assert response.data["count"] == 0


@pytest.mark.django_db
def test_clinic_create_is_owned_by_authenticated_user(location_tree):
    region, district = location_tree
    owner = User.objects.create_user(email="clinic-owner@example.tz", password="StrongPassword123!")
    client = APIClient()
    client.force_authenticate(user=owner)
    response = client.post("/api/v1/professionals/clinics/", {"name": "Healthy Paws", "registration_number": "CL-001", "region": region.pk, "district": district.pk, "phone_number": "+255700000000", "address": "Arusha"}, format="json")
    assert response.status_code == 201
    assert Clinic.objects.get(registration_number="CL-001").owner_id == owner.pk
