from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.api.views import LoginView, MeView, PasswordChangeView, RegisterView, ResendEmailVerificationView, VerifyEmailView
from accounts.api.admin_views import AdminUserDeleteView, AdminUserDetailView, AdminUserListView, AdminUserReactivateView, AdminUserSuspendView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="auth-register"),
    path("verify-email/", VerifyEmailView.as_view(), name="auth-verify-email"),
    path("verify-email/resend/", ResendEmailVerificationView.as_view(), name="auth-resend-email-verification"),
    path("login/", LoginView.as_view(), name="auth-login"),
    path("refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("me/", MeView.as_view(), name="user-me"),
    path("me/password/", PasswordChangeView.as_view(), name="user-password-change"),
    path("admin/users/", AdminUserListView.as_view(), name="admin-user-list"),
    path("admin/users/<uuid:pk>/", AdminUserDetailView.as_view(), name="admin-user-detail"),
    path("admin/users/<uuid:pk>/suspend/", AdminUserSuspendView.as_view(), name="admin-user-suspend"),
    path("admin/users/<uuid:pk>/reactivate/", AdminUserReactivateView.as_view(), name="admin-user-reactivate"),
    path("admin/users/<uuid:pk>/delete/", AdminUserDeleteView.as_view(), name="admin-user-delete"),
]
