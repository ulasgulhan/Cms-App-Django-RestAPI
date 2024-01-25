from rest_framework.permissions import BasePermission

class IsSuperUser(BasePermission):
    message = 'You must be admin permisson for this page'

    def has_permission(self, request, view):
        return request.user.is_superuser