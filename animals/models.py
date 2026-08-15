import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from professionals.models import ProfessionalProfile, Clinic


class AnimalSpecies(models.TextChoices):
    CATTLE = "CATTLE", "Cattle"
    GOAT = "GOAT", "Goat"
    SHEEP = "SHEEP", "Sheep"
    POULTRY = "POULTRY", "Poultry"
    DOG = "DOG", "Dog"
    CAT = "CAT", "Cat"
    OTHER = "OTHER", "Other"


class Animal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="animals")
    name = models.CharField(max_length=120)
    species = models.CharField(max_length=20, choices=AnimalSpecies.choices)
    breed = models.CharField(max_length=120, blank=True)
    sex = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    identification_code = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "id"]
        constraints = [models.UniqueConstraint(fields=["owner", "identification_code"], name="unique_animal_identifier_per_owner")]
        indexes = [models.Index(fields=["owner", "species", "is_active"])]


class VeterinaryRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name="records")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="authored_veterinary_records")
    clinic = models.ForeignKey(Clinic, null=True, blank=True, on_delete=models.PROTECT, related_name="veterinary_records")
    professional = models.ForeignKey(ProfessionalProfile, null=True, blank=True, on_delete=models.PROTECT, related_name="veterinary_records")
    record_type = models.CharField(max_length=80)
    title = models.CharField(max_length=180)
    body = models.TextField()
    occurred_at = models.DateTimeField(default=timezone.now)
    is_sensitive = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at", "id"]
        indexes = [models.Index(fields=["animal", "occurred_at"]), models.Index(fields=["author", "created_at"])]


class RecordAccessGrant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(VeterinaryRecord, on_delete=models.CASCADE, related_name="access_grants")
    granted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="grants_issued")
    grantee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="record_grants")
    permission = models.CharField(max_length=20, choices=[("READ", "Read"), ("WRITE", "Write")], default="READ")
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["record", "grantee"], name="unique_record_grantee")]
        indexes = [models.Index(fields=["grantee", "revoked_at", "expires_at"])]

    @property
    def is_active(self):
        return self.revoked_at is None and (self.expires_at is None or self.expires_at > timezone.now())


class RecordAccessLog(models.Model):
    record = models.ForeignKey(VeterinaryRecord, on_delete=models.CASCADE, related_name="access_logs")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="record_access_logs")
    action = models.CharField(max_length=30)
    occurred_at = models.DateTimeField(auto_now_add=True)
    request_id = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [models.Index(fields=["record", "occurred_at"])]
