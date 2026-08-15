from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    required_roles: tuple[str, ...] = ()

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_superuser or any(request.user.has_role(role) for role in self.required_roles)))


class IsAdministrator(HasRole):
    required_roles = ("ADMINISTRATOR",)


class IsOwnerOrAdministrator(BasePermission):
    owner_field = "user"

    def has_object_permission(self, request, view, obj):
        return bool(request.user.is_authenticated and (request.user.is_superuser or getattr(obj, self.owner_field, None) == request.user))
