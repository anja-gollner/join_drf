from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        is_staff = bool(request.user and request.user.is_staff)
        return is_staff or request.method in SAFE_METHODS


class IsAdminForDeleteOrPatchAndReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return bool(request.user and request.user.is_superuser)
        else:
            return bool(request.user and request.user.is_staff)


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == "DELETE":
            return bool(request.user and request.user.is_superuser)
        else:
            return bool(request.user and request.user == obj.user)


class IsSuperUserCRUDIsStaffCRUIsActiveOnlyRead(BasePermission):
    """
    Nur Superuser dürfen löschen.
    Staff darf alles außer löschen.
    Gäste dürfen nur GET-Anfragen stellen.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not (request.user.is_superuser or request.user.is_staff):
            return False
        if request.method == 'DELETE':
            return request.user and request.user.is_superuser
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'DELETE':
            return request.user and request.user.is_superuser
        return request.user and request.user.is_staff


class IsStaffOrSuperUserForTasks(BasePermission):
    """
    Superuser und Staff dürfen alle Operationen für Tasks durchführen.
     Gäste dürfen nur GET-Anfragen stellen.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_superuser or request.user.is_staff
