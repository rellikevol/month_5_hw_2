from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.pk, "   ", request.user.pk)
        return bool(obj.pk == request.user.pk)

class TransactionPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.from_user)
        return bool(obj.from_user.id == request.user.pk)
