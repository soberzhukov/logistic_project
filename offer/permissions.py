from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        """Создание и получение всех элементов доступно всем"""
        return True

    def has_object_permission(self, request, view, obj):
        """Можно изменять только владельцу"""
        return request.user == obj.author



