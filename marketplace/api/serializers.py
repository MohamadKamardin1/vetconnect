from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from marketplace.models import InventoryItem, Product, ProductInquiry, Vendor
from professionals.models import VerificationStatus


class PublicVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["id", "name", "description", "verification_status"]
        read_only_fields = fields


class PublicProductSerializer(serializers.ModelSerializer):
    vendor_name = serializers.CharField(source="vendor.name", read_only=True)
    availability = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "vendor", "vendor_name", "name", "category", "description", "price_amount", "currency", "requires_prescription", "availability"]
        read_only_fields = ["id", "vendor_name", "availability"]

    @extend_schema_field(serializers.CharField())
    def get_availability(self, obj):
        inventory = getattr(obj, "inventory", None)
        return inventory.availability if inventory else "UNKNOWN"


class ProductInquirySerializer(serializers.ModelSerializer):
    customer = serializers.CharField(source="customer.display_name", read_only=True)

    class Meta:
        model = ProductInquiry
        fields = ["id", "product", "customer", "quantity_requested", "message", "status", "created_at"]
        read_only_fields = ["id", "customer", "status", "created_at"]


class InventoryUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)
    low_stock_threshold = serializers.IntegerField(min_value=0, required=False, default=5)


class VendorProductWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "vendor", "sku", "name", "category", "description", "price_amount", "currency", "requires_prescription", "is_active", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_vendor(self, vendor):
        request = self.context["request"]
        if vendor.owner_id != request.user.pk:
            raise serializers.ValidationError("You can only manage your own vendor catalog.")
        if vendor.verification_status != VerificationStatus.VERIFIED:
            raise serializers.ValidationError("Vendor verification is required before listing products.")
        return vendor
