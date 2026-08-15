from decimal import Decimal
import pytest
from rest_framework.test import APIClient
from locations.models import District, Locality, Region, Territory, Ward


@pytest.mark.django_db
def test_location_hierarchy_and_territory_filtering():
    mainland = Region.objects.create(code="DAR", name="Dar es Salaam", territory=Territory.MAINLAND)
    zanzibar = Region.objects.create(code="SMZ", name="Mjini Magharibi", territory=Territory.ZANZIBAR)
    district = District.objects.create(region=mainland, code="ILALA", name="Ilala")
    ward = Ward.objects.create(district=district, code="KIVUKONI", name="Kivukoni")
    locality = Locality.objects.create(ward=ward, name="Central", latitude=Decimal("-6.81600"), longitude=Decimal("39.28000"))
    response = APIClient().get("/api/v1/locations/regions/?territory=ZANZIBAR")
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["code"] == zanzibar.code

    locality_response = APIClient().get("/api/v1/locations/localities/")
    coordinates = locality_response.data["results"][0]["public_coordinates"]
    assert coordinates["latitude"] == -6.82
    assert coordinates["longitude"] == 39.28
    assert coordinates["radius_km"] == 5.0
