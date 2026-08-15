from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from accounts.permissions import IsAdministrator
from marketplace.api.serializers import InventoryUpdateSerializer, ProductInquirySerializer, PublicProductSerializer, PublicVendorSerializer, VendorProductWriteSerializer
from marketplace.models import InventoryItem, Product, ProductInquiry, Vendor
from professionals.models import VerificationStatus


class PublicProductListView(generics.ListAPIView):
    serializer_class = PublicProductSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Product.objects.filter(is_active=True, vendor__is_active=True, vendor__verification_status=VerificationStatus.VERIFIED).select_related("vendor").prefetch_related("inventory")


class PublicProductDetailView(generics.RetrieveAPIView):
    serializer_class = PublicProductSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Product.objects.filter(is_active=True, vendor__is_active=True, vendor__verification_status=VerificationStatus.VERIFIED).select_related("vendor").prefetch_related("inventory")


class VendorProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        return VendorProductWriteSerializer

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return Product.objects.none()
        return Product.objects.filter(vendor__owner=self.request.user).select_related("vendor")


class ProductInquiryCreateView(generics.CreateAPIView):
    serializer_class = ProductInquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.request.data.get("product"), is_active=True, vendor__is_active=True, vendor__verification_status=VerificationStatus.VERIFIED)
        serializer.save(customer=self.request.user, product=product)


class ProductInquiryListView(generics.ListAPIView):
    serializer_class = ProductInquirySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return ProductInquiry.objects.none()
        return ProductInquiry.objects.filter(customer=self.request.user) | ProductInquiry.objects.filter(product__vendor__owner=self.request.user)


class InventoryUpdateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InventoryUpdateSerializer

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk, vendor__owner=request.user)
        payload = self.get_serializer(data=request.data)
        payload.is_valid(raise_exception=True)
        quantity = payload.validated_data["quantity"]
        threshold = payload.validated_data.get("low_stock_threshold", 5)
        item, _ = InventoryItem.objects.update_or_create(product=product, defaults={"quantity": quantity, "low_stock_threshold": threshold})
        return Response({"product": str(product.pk), "availability": item.availability, "updated": True})
