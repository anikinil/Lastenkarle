from rest_framework import permissions
from db_model.models import User_Flag


class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if request.user.is_staff and user.is_staff_of_store() is not None:
            return True
        return False


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if request.user.is_superuser and user.user_flags.contains(User_Flag.objects.get(flag='Administrator')):
            return True
        return False


class IsVerfied(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if user.user_flags.contains(User_Flag.objects.get(flag='Verified')):
            return True
        return False
