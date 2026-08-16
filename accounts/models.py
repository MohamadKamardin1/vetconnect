import hashlib
import secrets
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import IntegrityError, models
from django.utils.crypto import salted_hmac
from django.utils import timezone


class RoleCode(models.TextChoices):
    OWNER = "OWNER", "Owner"
    FARMER = "FARMER", "Farmer"
    VETERINARIAN = "VETERINARIAN", "Veterinarian"
    PARAPROFESSIONAL = "PARAPROFESSIONAL", "Paraprofessional"
    CLINIC_OWNER = "CLINIC_OWNER", "Clinic owner"
    CLINIC_STAFF = "CLINIC_STAFF", "Clinic staff"
    VENDOR = "VENDOR", "Vendor"
    MODERATOR = "MODERATOR", "Moderator"
    CONTENT_MANAGER = "CONTENT_MANAGER", "Content manager"
    SUPPORT_OPERATOR = "SUPPORT_OPERATOR", "Support operator"
    ADMINISTRATOR = "ADMINISTRATOR", "Administrator"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        user = self.create_user(email, password, **extra_fields)
        user.assign_role(RoleCode.ADMINISTRATOR)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email_verified_at = models.DateTimeField(null=True, blank=True)
    phone_verified_at = models.DateTimeField(null=True, blank=True)
    suspended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["email", "is_active"]), models.Index(fields=["phone_number", "is_active"])]

    def assign_role(self, code, assigned_by=None):
        role, _ = Role.objects.get_or_create(code=code, defaults={"name": code.replace("_", " ").title()})
        return UserRole.objects.get_or_create(user=self, role=role, defaults={"assigned_by": assigned_by})[0]

    def has_role(self, code):
        return self.user_roles.filter(role__code=code, is_active=True).exists()

    @property
    def display_name(self):
        return (f"{self.first_name} {self.last_name}").strip() or self.email


class Role(models.Model):
    code = models.CharField(max_length=40, choices=RoleCode.choices, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="user_roles")
    assigned_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_roles")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "role"], name="unique_user_role")]
        indexes = [models.Index(fields=["user", "is_active"]), models.Index(fields=["role", "is_active"])]


class OneTimeToken(models.Model):
    class Purpose(models.TextChoices):
        EMAIL_VERIFY = "EMAIL_VERIFY", "Email verification"
        PHONE_VERIFY = "PHONE_VERIFY", "Phone verification"
        PASSWORD_RESET = "PASSWORD_RESET", "Password reset"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="one_time_tokens")
    purpose = models.CharField(max_length=30, choices=Purpose.choices)
    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    attempt_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def issue(cls, user, purpose, ttl_minutes=15):
        raw = secrets.token_urlsafe(32)
        instance = cls.objects.create(user=user, purpose=purpose, token_hash=hashlib.sha256(raw.encode()).hexdigest(), expires_at=timezone.now() + timedelta(minutes=ttl_minutes))
        return instance, raw

    def consume(self, raw):
        if self.used_at or self.expires_at <= timezone.now():
            return False
        if not secrets.compare_digest(self.token_hash, hashlib.sha256(raw.encode()).hexdigest()):
            return False
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])
        return True

    @classmethod
    def issue_email_code(cls, user, *, ttl_minutes=10):
        """Create a six-digit verification code without ever storing the raw value."""
        for _ in range(5):
            code = f"{secrets.randbelow(1_000_000):06d}"
            token_hash = salted_hmac("accounts.email-verification-code", f"{user.pk}:{code}").hexdigest()
            try:
                return cls.objects.create(
                    user=user,
                    purpose=cls.Purpose.EMAIL_VERIFY,
                    token_hash=token_hash,
                    expires_at=timezone.now() + timedelta(minutes=ttl_minutes),
                ), code
            except IntegrityError:
                continue
        raise RuntimeError("Could not create a unique email verification code.")

    def matches_email_code(self, code):
        candidate = salted_hmac("accounts.email-verification-code", f"{self.user_id}:{code}").hexdigest()
        return secrets.compare_digest(self.token_hash, candidate)
