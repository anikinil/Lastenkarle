from rest_framework import permissions


SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


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
