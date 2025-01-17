from rest_framework import permissions
from db_model.models import User_Flag, Store


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        store_name = view.kwargs.get('store_name')
        if not Store.objects.filter(name=store_name).exists():
            return False
        store = Store.objects.get(name=store_name)
        if request.user.is_staff and user.user_flags.contains(store.store_flag):
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
