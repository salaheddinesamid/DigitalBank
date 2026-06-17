from rest_framework.permissions import BasePermission


class HasRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        # Check if the HTTP request has an authentication
        if not request.user.is_authenticated:
            return False

        # Extract the roles:
        user_roles = request.user.roles.values_list(
            'role_name',
            flat=True
        )

        # Check if the user has at least one allowed role
        return any(role in user_roles for role in self.allowed_roles)


class IsCustomer(HasRole):
    allowed_roles = ["CUSTOMER"]


class IsBanker(HasRole):
    allowed_roles = ["BANKER"]