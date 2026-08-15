from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from locations.models import District, Locality, Region, ServiceArea, Ward


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["code", "name", "territory"]


class DistrictSerializer(serializers.ModelSerializer):
    region_code = serializers.CharField(source="region.code", read_only=True)

    class Meta:
        model = District
        fields = ["code", "name", "region_code"]


class WardSerializer(serializers.ModelSerializer):
    district_code = serializers.CharField(source="district.code", read_only=True)

    class Meta:
        model = Ward
        fields = ["code", "name", "district_code"]


class LocalitySerializer(serializers.ModelSerializer):
    ward_code = serializers.CharField(source="ward.code", read_only=True)
    public_coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Locality
        fields = ["id", "name", "postal_code", "ward_code", "public_coordinates"]

    @extend_schema_field(serializers.DictField(allow_null=True))
    def get_public_coordinates(self, obj):
        return obj.public_coordinates()


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = ["id", "name", "territory"]
