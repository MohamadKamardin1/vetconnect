from django.urls import path
from marketplace.api.views import InventoryUpdateView, ProductInquiryCreateView, ProductInquiryListView, PublicProductDetailView, PublicProductListView, VendorProductListCreateView

urlpatterns = [
    path("products/", PublicProductListView.as_view(), name="public-product-list"),
    path("products/<uuid:pk>/", PublicProductDetailView.as_view(), name="public-product-detail"),
    path("vendor/products/", VendorProductListCreateView.as_view(), name="vendor-product-list-create"),
    path("products/<uuid:pk>/inventory/", InventoryUpdateView.as_view(), name="product-inventory-update"),
    path("inquiries/", ProductInquiryListView.as_view(), name="inquiry-list"),
    path("inquiries/create/", ProductInquiryCreateView.as_view(), name="inquiry-create"),
]
