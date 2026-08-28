import pytest
from rest_framework.test import APIClient

from accounts.models import User
from marketplace.models import InventoryItem, Product, ProductInquiry, Vendor
from professionals.models import VerificationStatus


def _client(email):
    user = User.objects.create_user(email=email, password="StrongPass123!")
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user


def _verified_vendor(owner, name="Acme Vet Supplies", reg="REG-0001"):
    return Vendor.objects.create(owner=owner, name=name, registration_number=reg, verification_status=VerificationStatus.VERIFIED)


@pytest.mark.django_db
def test_vendor_product_list_is_owner_scoped_and_includes_id():
    """Regression test: the vendor product list serializer previously omitted `id`, making it
    impossible for a client to reference a listed product for any follow-up action (e.g. updating
    its inventory). Also confirms one vendor never sees another vendor's product in this endpoint."""
    client_a, owner_a = _client("vendor-a@example.com")
    _client_b, owner_b = _client("vendor-b@example.com")
    vendor_a = _verified_vendor(owner_a, name="Vendor A", reg="REG-A")
    vendor_b = _verified_vendor(owner_b, name="Vendor B", reg="REG-B")
    Product.objects.create(vendor=vendor_a, sku="A-1", name="Mine", category="feed", price_amount="1000.00")
    Product.objects.create(vendor=vendor_b, sku="B-1", name="NotMine", category="feed", price_amount="2000.00")

    response = client_a.get("/api/v1/marketplace/vendor/products/")
    assert response.status_code == 200
    results = response.data["results"]
    assert len(results) == 1
    assert results[0]["name"] == "Mine"
    assert "id" in results[0] and results[0]["id"]  # the regression this test guards against


@pytest.mark.django_db
def test_vendor_cannot_create_product_for_another_vendor():
    client_a, owner_a = _client("vendor-c@example.com")
    _client_b, owner_b = _client("vendor-d@example.com")
    _vendor_a = _verified_vendor(owner_a, name="Vendor C", reg="REG-C")
    vendor_b = _verified_vendor(owner_b, name="Vendor D", reg="REG-D")

    response = client_a.post("/api/v1/marketplace/vendor/products/", {"vendor": str(vendor_b.pk), "sku": "X-1", "name": "Hijack", "category": "feed"}, format="json")
    assert response.status_code == 400
    assert not Product.objects.filter(sku="X-1").exists()


@pytest.mark.django_db
def test_public_product_list_excludes_unverified_vendor():
    owner = User.objects.create_user(email="vendor-e@example.com", password="StrongPass123!")
    unverified_vendor = Vendor.objects.create(owner=owner, name="Pending Vendor", registration_number="REG-E", verification_status=VerificationStatus.SUBMITTED)
    Product.objects.create(vendor=unverified_vendor, sku="P-1", name="NotYetPublic", category="feed")

    response = APIClient().get("/api/v1/marketplace/products/")
    assert response.status_code == 200
    names = [p["name"] for p in response.data["results"]]
    assert "NotYetPublic" not in names


@pytest.mark.django_db
def test_inventory_update_is_owner_scoped():
    client_a, owner_a = _client("vendor-f@example.com")
    _client_b, owner_b = _client("vendor-g@example.com")
    vendor_a = _verified_vendor(owner_a, name="Vendor F", reg="REG-F")
    vendor_b = _verified_vendor(owner_b, name="Vendor G", reg="REG-G")
    product_b = Product.objects.create(vendor=vendor_b, sku="G-1", name="NotYours", category="feed")

    response = client_a.patch(f"/api/v1/marketplace/products/{product_b.pk}/inventory/", {"quantity": 999}, format="json")
    assert response.status_code == 404
    assert not InventoryItem.objects.filter(product=product_b).exists()


@pytest.mark.django_db
def test_inquiry_list_is_scoped_to_customer_or_owning_vendor():
    customer_client, customer = _client("customer-a@example.com")
    vendor_client, vendor_owner = _client("vendor-h@example.com")
    _outsider_client, outsider = _client("outsider@example.com")
    vendor = _verified_vendor(vendor_owner, name="Vendor H", reg="REG-H")
    product = Product.objects.create(vendor=vendor, sku="H-1", name="Item", category="feed")
    inquiry = ProductInquiry.objects.create(product=product, customer=customer, message="Is this in stock?")

    outsider_response = _outsider_client.get("/api/v1/marketplace/inquiries/")
    assert outsider_response.data["count"] == 0

    customer_response = customer_client.get("/api/v1/marketplace/inquiries/")
    assert customer_response.data["count"] == 1

    vendor_response = vendor_client.get("/api/v1/marketplace/inquiries/")
    assert vendor_response.data["count"] == 1
    assert vendor_response.data["results"][0]["id"] == str(inquiry.pk)


@pytest.mark.django_db
def test_inquiry_create_rejected_for_unverified_vendor_product():
    customer_client, _customer = _client("customer-b@example.com")
    owner = User.objects.create_user(email="vendor-i@example.com", password="StrongPass123!")
    unverified_vendor = Vendor.objects.create(owner=owner, name="Vendor I", registration_number="REG-I", verification_status=VerificationStatus.DRAFT)
    product = Product.objects.create(vendor=unverified_vendor, sku="I-1", name="NotSellable", category="feed")

    response = customer_client.post("/api/v1/marketplace/inquiries/create/", {"product": str(product.pk), "message": "Interested"}, format="json")
    assert response.status_code == 404
    assert not ProductInquiry.objects.filter(product=product).exists()
