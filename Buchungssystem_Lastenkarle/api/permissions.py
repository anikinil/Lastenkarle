from rest_framework import permissions
from db_model.models import User_Status


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return False


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class IsVerfied(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.user_status.contains(User_Status.objects.get(user_status='Verified')):
            return True
        return False
