from rest_framework_simplejwt import permissions

class IsHost(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.host == request.user
