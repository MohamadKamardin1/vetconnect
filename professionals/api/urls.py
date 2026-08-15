from django.urls import path
from professionals.api.views import ClinicListCreateView, CredentialCreateView, CredentialListView, KYCReviewView, ProfessionalCreateView, ProfessionalListView, ProfessionalMeView

urlpatterns = [
    path("professionals/", ProfessionalListView.as_view(), name="professional-list"),
    path("professionals/me/", ProfessionalMeView.as_view(), name="professional-me"),
    path("professionals/apply/", ProfessionalCreateView.as_view(), name="professional-apply"),
    path("professionals/<uuid:pk>/review/", KYCReviewView.as_view(), name="professional-kyc-review"),
    path("clinics/", ClinicListCreateView.as_view(), name="clinic-list-create"),
    path("credentials/", CredentialListView.as_view(), name="credential-list"),
    path("credentials/upload/", CredentialCreateView.as_view(), name="credential-upload"),
]
