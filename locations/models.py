from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Territory(models.TextChoices):
    MAINLAND = "MAINLAND", "Tanzania Mainland"
    ZANZIBAR = "ZANZIBAR", "Zanzibar"


class Region(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=160)
    territory = models.CharField(max_length=20, choices=Territory.choices)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["territory", "name"]
        indexes = [models.Index(fields=["territory", "is_active"])]


class District(models.Model):
    region = models.ForeignKey(Region, on_delete=models.PROTECT, related_name="districts")
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=160)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["region", "code"], name="unique_district_code_per_region")]
        indexes = [models.Index(fields=["region", "is_active"])]


class Ward(models.Model):
    district = models.ForeignKey(District, on_delete=models.PROTECT, related_name="wards")
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=160)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["district", "code"], name="unique_ward_code_per_district")]
        indexes = [models.Index(fields=["district", "is_active"])]


class Locality(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.PROTECT, related_name="localities")
    name = models.CharField(max_length=160)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True, validators=[MinValueValidator(Decimal("-12.0")), MaxValueValidator(Decimal("-0.5"))])
    longitude = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True, validators=[MinValueValidator(Decimal("29.0")), MaxValueValidator(Decimal("41.0"))])
    public_radius_km = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("5.00"), validators=[MinValueValidator(Decimal("0.10")), MaxValueValidator(Decimal("100.00"))])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name", "id"]
        constraints = [models.UniqueConstraint(fields=["ward", "name"], name="unique_locality_per_ward")]
        indexes = [models.Index(fields=["ward", "is_active"]), models.Index(fields=["latitude", "longitude"])]

    def public_coordinates(self):
        if self.latitude is None or self.longitude is None:
            return None
        return {"latitude": round(float(self.latitude), 2), "longitude": round(float(self.longitude), 2), "radius_km": float(self.public_radius_km)}


class ServiceArea(models.Model):
    name = models.CharField(max_length=160)
    territory = models.CharField(max_length=20, choices=Territory.choices)
    regions = models.ManyToManyField(Region, blank=True, related_name="service_areas")
    districts = models.ManyToManyField(District, blank=True, related_name="service_areas")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
