from rest_framework.permissions import BasePermission


class HasCustomerDatabaseAccessOrIsSuperUser(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return (
            request.user.customer_database_access or request.user.is_superuser
        )
