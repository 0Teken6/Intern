from rest_framework import permissions


class IsOwnerOrReaderOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    

class IsAuthorOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role not in ('author') or not request.user.is_superuser:
            return False
        return super().has_permission(request, view)