"""Check permissions with role-based access control."""

from collections.abc import Iterable

from masoon.errors import PermissionDeniedError
from masoon.storage.protocols import RoleAssignmentStore
from masoon.types import Identity, Role


class Authorizer:
    """Decide whether an identity is allowed to perform an action.

    Roles are defined in code and passed in when the authorizer is created.
    The role assignment store only records which role names each user has.

    Access is denied by default: a user with no roles, or with role names
    that are not defined, has no permissions.
    """

    def __init__(self, roles: Iterable[Role], assignments: RoleAssignmentStore) -> None:
        """Initialize the authorizer with the defined roles and an assignment store.

        Raises:
            ValueError: If two roles have the same name.

        """
        self._roles: dict[str, Role] = {}
        for role in roles:
            if role.name in self._roles:
                msg = f"Duplicate role name: {role.name}"
                raise ValueError(msg)
            self._roles[role.name] = role

        self._assignments = assignments

    def permissions_for(self, identity: Identity) -> frozenset[str]:
        """Return every permission granted to the identity through its roles.

        Role names that are not defined are ignored.
        """
        permissions: set[str] = set()
        for role_name in self._assignments.get_roles(identity.id):
            role = self._roles.get(role_name)
            if role is not None:
                permissions |= role.permissions
        return frozenset(permissions)

    def has_permission(self, identity: Identity, permission: str) -> bool:
        """Return whether the identity has the permission."""
        return permission in self.permissions_for(identity)

    def require(self, identity: Identity, permission: str) -> None:
        """Raise an error unless the identity has the permission.

        Raises:
            PermissionDeniedError: If the identity does not have the permission.

        """
        if not self.has_permission(identity, permission):
            raise PermissionDeniedError(permission)
