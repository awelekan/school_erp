from rest_framework.permissions import BasePermission

class IsSuperadminOrControllerOrAccountant(BasePermission):
    """
    Custom permission to grant access only to Superadmin, Controller, or Accountant.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superadmin() or request.user.is_controller() or request.user.is_accountant()
        )
