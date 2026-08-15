from rest_framework import generics, permissions
from locations.api.serializers import DistrictSerializer, LocalitySerializer, RegionSerializer, ServiceAreaSerializer, WardSerializer
from locations.models import District, Locality, Region, ServiceArea, Ward


class PublicListMixin:
    permission_classes = [permissions.AllowAny]
    authentication_classes = []


class RegionListView(PublicListMixin, generics.ListAPIView):
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer
    filterset_fields = ["territory", "code"]
    search_fields = ["name", "code"]


class DistrictListView(PublicListMixin, generics.ListAPIView):
    queryset = District.objects.filter(is_active=True).select_related("region")
    serializer_class = DistrictSerializer
    filterset_fields = ["region__code", "region__territory", "code"]
    search_fields = ["name", "code"]


class WardListView(PublicListMixin, generics.ListAPIView):
    queryset = Ward.objects.filter(is_active=True).select_related("district")
    serializer_class = WardSerializer
    filterset_fields = ["district__code", "district__region__code", "code"]
    search_fields = ["name", "code"]


class LocalityListView(PublicListMixin, generics.ListAPIView):
    queryset = Locality.objects.filter(is_active=True).select_related("ward")
    serializer_class = LocalitySerializer
    filterset_fields = ["ward__code", "ward__district__code"]
    search_fields = ["name", "postal_code"]


class ServiceAreaListView(PublicListMixin, generics.ListAPIView):
    queryset = ServiceArea.objects.filter(is_active=True)
    serializer_class = ServiceAreaSerializer
    filterset_fields = ["territory"]
    search_fields = ["name"]
