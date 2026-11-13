"""Define shared types used throughout Masoon."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Identity:
    """Represent the identity of an authenticated user."""

    id: str
    username: str


@dataclass(frozen=True, slots=True)
class Role:
    """Represent a named role and the permissions it grants.

    Permissions are plain strings, such as ``"posts:edit"``, and are matched
    exactly. They are always stored as a ``frozenset``, so the permissions of a
    role cannot change after it is created, even if another collection was
    passed in.
    """

    name: str
    permissions: frozenset[str]

    def __post_init__(self) -> None:
        """Store the permissions as a frozenset and check that they are strings.

        Raises:
            TypeError: If the permissions are a single string instead of a
                collection, or if any permission is not a string.

        """
        if isinstance(self.permissions, str):
            msg = "Role permissions must be a collection of strings, not a single string."
            raise TypeError(msg)

        permissions = frozenset(self.permissions)
        if not all(isinstance(permission, str) for permission in permissions):
            msg = "Every role permission must be a string."
            raise TypeError(msg)

        object.__setattr__(self, "permissions", permissions)
