"""Security-sensitive email verification services for account activation."""
import logging
from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone

from accounts.models import OneTimeToken, User

logger = logging.getLogger(__name__)


class EmailVerificationError(Exception):
    """Base class for intentionally generic verification failures."""


class EmailVerificationRateLimited(EmailVerificationError):
    def __init__(self, retry_after_seconds=0):
        self.retry_after_seconds = max(0, int(retry_after_seconds))
        super().__init__("A verification code was sent recently.")


class EmailVerificationDeliveryError(EmailVerificationError):
    pass


def _send_verification_email(*, user, code):
    ttl_minutes = settings.EMAIL_VERIFICATION_CODE_TTL_MINUTES
    send_mail(
        subject="Your VetKonnect verification code",
        message=(
            f"Hello {user.display_name},\n\n"
            f"Your VetKonnect verification code is: {code}\n\n"
            f"It expires in {ttl_minutes} minutes. Do not share this code with anyone. "
            "VetKonnect staff will never ask for it.\n\n"
            "If you did not create this account, you can safely ignore this email."
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def issue_email_verification_code(user):
    """Invalidate older codes, apply resend limits, then send a fresh six-digit code."""
    now = timezone.now()
    cooldown_seconds = settings.EMAIL_VERIFICATION_RESEND_COOLDOWN_SECONDS
    rolling_window_start = now - timedelta(hours=1)

    with transaction.atomic():
        user = User.objects.select_for_update().get(pk=user.pk)
        if user.email_verified_at or user.is_active:
            raise EmailVerificationError("This account is not awaiting verification.")

        previous = user.one_time_tokens.filter(
            purpose=OneTimeToken.Purpose.EMAIL_VERIFY,
        ).order_by("-created_at").first()
        if previous:
            elapsed = (now - previous.created_at).total_seconds()
            if elapsed < cooldown_seconds:
                raise EmailVerificationRateLimited(cooldown_seconds - elapsed)

        recent_count = user.one_time_tokens.filter(
            purpose=OneTimeToken.Purpose.EMAIL_VERIFY,
            created_at__gte=rolling_window_start,
        ).count()
        if recent_count >= settings.EMAIL_VERIFICATION_MAX_CODES_PER_HOUR:
            raise EmailVerificationRateLimited(int((previous.created_at + timedelta(hours=1) - now).total_seconds()))

        user.one_time_tokens.filter(
            purpose=OneTimeToken.Purpose.EMAIL_VERIFY,
            used_at__isnull=True,
        ).update(used_at=now)
        token, code = OneTimeToken.issue_email_code(
            user,
            ttl_minutes=settings.EMAIL_VERIFICATION_CODE_TTL_MINUTES,
        )

    try:
        _send_verification_email(user=user, code=code)
    except Exception as exc:  # SMTP outages are safe to retry through the resend endpoint.
        logger.exception("Email verification delivery failed for user_id=%s", user.pk)
        token.used_at = timezone.now()
        token.save(update_fields=["used_at"])
        raise EmailVerificationDeliveryError("Unable to send a verification email right now.") from exc

    return token


def anonymize_user(user):
    """
    Irreversibly scrub personally-identifying fields on a user record without deleting the row,
    preserving referential integrity for everything that references it (animals, assessments,
    audit entries, etc.). Shared by administrator-triggered deletion (accounts.api.admin_views)
    and self-service deletion (privacy.services.confirm_deletion) so both paths anonymize
    identically rather than maintaining two copies of security-sensitive scrubbing logic.
    """
    user.is_active = False
    user.email = f"deleted+{user.pk}@invalid.local"
    user.phone_number = None
    user.first_name = "Deleted"
    user.last_name = "User"
    user.set_unusable_password()
    user.save(update_fields=["is_active", "email", "phone_number", "first_name", "last_name", "password", "updated_at"])
    return user


def verify_email_code(*, email, code):
    """Verify a code atomically and activate the matching pending account."""
    now = timezone.now()
    invalid_code = False
    with transaction.atomic():
        user = User.objects.select_for_update().filter(email__iexact=email).first()
        if not user or user.is_active or user.email_verified_at:
            invalid_code = True
        else:
            token = user.one_time_tokens.select_for_update().filter(
                purpose=OneTimeToken.Purpose.EMAIL_VERIFY,
                used_at__isnull=True,
                expires_at__gt=now,
            ).order_by("-created_at").first()
            if not token:
                invalid_code = True
            elif token.attempt_count >= settings.EMAIL_VERIFICATION_MAX_ATTEMPTS or not token.matches_email_code(code):
                token.attempt_count += 1
                update_fields = ["attempt_count"]
                if token.attempt_count >= settings.EMAIL_VERIFICATION_MAX_ATTEMPTS:
                    token.used_at = now
                    update_fields.append("used_at")
                token.save(update_fields=update_fields)
                invalid_code = True
            else:
                token.used_at = now
                token.save(update_fields=["used_at"])
                user.is_active = True
                user.email_verified_at = now
                user.save(update_fields=["is_active", "email_verified_at", "updated_at"])

    if invalid_code:
        raise EmailVerificationError("Invalid or expired verification code.")
    return user
