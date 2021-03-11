from rest_framework import permissions
from django.conf import settings


class IsLoggedIn(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.username not in settings.LOGOUT_USERS_SET)
