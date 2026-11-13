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
    exactly. Use a ``frozenset`` so the permissions of a role cannot change
    after it is created.
    """

    name: str
    permissions: frozenset[str]
