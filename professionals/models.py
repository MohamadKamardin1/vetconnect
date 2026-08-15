import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from locations.models import District, Region, ServiceArea


class VerificationStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    SUBMITTED = "SUBMITTED", "Submitted"
    IN_REVIEW = "IN_REVIEW", "In review"
    VERIFIED = "VERIFIED", "Verified"
    REJECTED = "REJECTED", "Rejected"
    SUSPENDED = "SUSPENDED", "Suspended"


class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="owned_clinics")
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=80, unique=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="clinics")
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="clinics")
    service_area = models.ForeignKey(ServiceArea, null=True, blank=True, on_delete=models.SET_NULL, related_name="clinics")
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.DRAFT)
    verified_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [models.Index(fields=["region", "district", "verification_status"])]


class ProfessionalProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="professional_profile")
    professional_type = models.CharField(max_length=40)
    registration_number = models.CharField(max_length=80, unique=True)
    issuing_body = models.CharField(max_length=160)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="professionals")
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="professionals")
    bio = models.TextField(blank=True)
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.DRAFT)
    verified_at = models.DateTimeField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__last_name", "user__first_name", "id"]
        indexes = [models.Index(fields=["region", "district", "verification_status", "is_available"])]

    @property
    def is_publicly_discoverable(self):
        return self.verification_status == VerificationStatus.VERIFIED and self.is_active


class ClinicStaff(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="staff_members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="clinic_memberships")
    title = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["clinic", "user"], name="unique_clinic_staff")]


class CredentialDocument(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="credential_documents")
    professional = models.ForeignKey(ProfessionalProfile, null=True, blank=True, on_delete=models.CASCADE, related_name="documents")
    clinic = models.ForeignKey(Clinic, null=True, blank=True, on_delete=models.CASCADE, related_name="documents")
    document_type = models.CharField(max_length=80)
    object_key = models.CharField(max_length=500)
    sha256 = models.CharField(max_length=64)
    mime_type = models.CharField(max_length=120)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=True)

    class Meta:
        ordering = ["-submitted_at", "id"]
        constraints = [models.CheckConstraint(condition=(models.Q(professional__isnull=False) | models.Q(clinic__isnull=False)), name="credential_has_subject")]
        indexes = [models.Index(fields=["owner", "submitted_at"])]


class KYCReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="kyc_reviews")
    professional = models.ForeignKey(ProfessionalProfile, null=True, blank=True, on_delete=models.CASCADE, related_name="reviews")
    clinic = models.ForeignKey(Clinic, null=True, blank=True, on_delete=models.CASCADE, related_name="kyc_reviews")
    decision = models.CharField(max_length=20, choices=VerificationStatus.choices)
    reason_code = models.CharField(max_length=80, blank=True)
    notes = models.TextField(blank=True)
    decided_at = models.DateTimeField(default=timezone.now)

    class Meta:
        indexes = [models.Index(fields=["decision", "decided_at"])]
