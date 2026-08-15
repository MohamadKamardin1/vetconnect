from datetime import timedelta
import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from accounts.models import User
from animals.models import Animal, RecordAccessGrant, VeterinaryRecord


@pytest.mark.django_db
def test_owner_can_create_and_other_user_cannot_see_animal():
    owner = User.objects.create_user(email='animal-owner@example.tz', password='StrongPassword123!')
    other = User.objects.create_user(email='animal-other@example.tz', password='StrongPassword123!')
    client = APIClient(); client.force_authenticate(user=owner)
    created = client.post('/api/v1/animals/animals/', {'name': 'Maziwa', 'species': 'CATTLE'}, format='json')
    assert created.status_code == 201
    client.force_authenticate(user=other)
    response = client.get('/api/v1/animals/animals/')
    assert response.data['count'] == 0


@pytest.mark.django_db
def test_record_grant_expiry_and_revocation_enforce_protected_access():
    owner = User.objects.create_user(email='record-owner@example.tz', password='StrongPassword123!')
    grantee = User.objects.create_user(email='record-grantee@example.tz', password='StrongPassword123!')
    animal = Animal.objects.create(owner=owner, name='Kuku', species='POULTRY')
    record = VeterinaryRecord.objects.create(animal=animal, author=owner, record_type='VISIT', title='Check', body='Protected')
    grant = RecordAccessGrant.objects.create(record=record, granted_by=owner, grantee=grantee, expires_at=timezone.now() + timedelta(hours=1))
    client = APIClient(); client.force_authenticate(user=grantee)
    assert client.get(f'/api/v1/animals/records/{record.pk}/').status_code == 200
    grant.expires_at = timezone.now() - timedelta(minutes=1); grant.save(update_fields=['expires_at'])
    assert client.get(f'/api/v1/animals/records/{record.pk}/').status_code == 404
    grant.expires_at = timezone.now() + timedelta(hours=1); grant.revoked_at = timezone.now(); grant.save(update_fields=['expires_at', 'revoked_at'])
    assert client.get(f'/api/v1/animals/records/{record.pk}/').status_code == 404
