from django.urls import path
from notifications.api.views import NotificationDetailView, NotificationListView, NotificationMarkReadView, NotificationPreferenceView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("preferences/", NotificationPreferenceView.as_view(), name="notification-preferences"),
    path("<uuid:pk>/", NotificationDetailView.as_view(), name="notification-detail"),
    path("<uuid:pk>/read/", NotificationMarkReadView.as_view(), name="notification-mark-read"),
]
