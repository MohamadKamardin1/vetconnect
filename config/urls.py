from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from core.api.views import HealthView, ReadinessView

handler400 = "core.views.error_400"
handler403 = "core.views.error_403"
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", HealthView.as_view(), name="health"),
    path("readiness/", ReadinessView.as_view(), name="readiness"),
    path("api/v1/auth/", include("accounts.api.urls")),
    path("api/v1/users/", include("accounts.api.urls")),
    path("api/v1/locations/", include("locations.api.urls")),
    path("api/v1/professionals/", include("professionals.api.urls")),
    path("api/v1/animals/", include("animals.api.urls")),
    path("api/v1/discovery/", include("discovery.api.urls")),
    path("api/v1/marketplace/", include("marketplace.api.urls")),
    path("api/v1/messaging/", include("messaging.api.urls")),
    path("api/v1/community/", include("community.api.urls")),
    path("api/v1/feed/", include("feed.api.urls")),
    path("api/v1/disease/", include("disease.api.urls")),
    path("api/v1/notifications/", include("notifications.api.urls")),
    path("api/v1/billing/", include("billing.api.urls")),
    path("api/v1/ai/", include("ai.api.urls")),
    path("api/v1/audit/", include("audit.api.urls")),
    path("api/v1/privacy/", include("privacy.api.urls")),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]
