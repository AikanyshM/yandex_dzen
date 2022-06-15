from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminorAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True


    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if obj.user == request.user:
            return True

        if request.user.is_staff and request.method == "DELETE":
            return True