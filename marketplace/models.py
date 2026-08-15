import uuid
from django.conf import settings
from django.db import models
from professionals.models import Clinic, VerificationStatus


class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="vendors")
    name = models.CharField(max_length=180)
    registration_number = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.DRAFT)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "id"]


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="products")
    sku = models.CharField(max_length=120)
    name = models.CharField(max_length=180)
    category = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    price_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="TZS")
    requires_prescription = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name", "id"]
        constraints = [models.UniqueConstraint(fields=["vendor", "sku"], name="unique_vendor_product_sku")]
        indexes = [models.Index(fields=["category", "is_active"])]


class InventoryItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    last_counted_at = models.DateTimeField(auto_now=True)

    @property
    def availability(self):
        if self.quantity <= 0:
            return "OUT_OF_STOCK"
        if self.quantity <= self.low_stock_threshold:
            return "LOW_STOCK"
        return "IN_STOCK"


class ProductInquiry(models.Model):
    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        RESPONDED = "RESPONDED", "Responded"
        CLOSED = "CLOSED", "Closed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="inquiries")
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="product_inquiries")
    quantity_requested = models.PositiveIntegerField(default=1)
    message = models.TextField(max_length=2000)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "id"]
