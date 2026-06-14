
from ..models import RoleNames, Role
from django.db import transaction


def test_roles():
    for key, label in RoleNames.choices:

        if not Role.objects.filter(
            role_name=key
        ).exists():
            role = Role.objects.create(
                role_name=key
            )

    print("All the roles are in the database:")
