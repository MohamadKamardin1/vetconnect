from django.urls import path
from locations.api.views import DistrictListView, LocalityListView, RegionListView, ServiceAreaListView, WardListView

urlpatterns = [
    path("regions/", RegionListView.as_view(), name="location-region-list"),
    path("districts/", DistrictListView.as_view(), name="location-district-list"),
    path("wards/", WardListView.as_view(), name="location-ward-list"),
    path("localities/", LocalityListView.as_view(), name="location-locality-list"),
    path("service-areas/", ServiceAreaListView.as_view(), name="location-service-area-list"),
]
