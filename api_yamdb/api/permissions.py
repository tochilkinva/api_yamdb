from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.role == request.user.UserRole.ADMIN
                or request.method in permissions.SAFE_METHODS
            )
        return request.method in permissions.SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                request.user.is_staff
                or request.user.role == request.user.UserRole.ADMIN
            )
        return False


class IsAuthorOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author
            or request.user.role == request.user.UserRole.ADMIN
            or request.user.role == request.user.UserRole.MODERATOR
            or request.user.is_superuser
        )
