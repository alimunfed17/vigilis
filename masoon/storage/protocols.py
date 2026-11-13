"""Define protocols that user, session, and role storage backends must implement."""

from datetime import datetime
from typing import Protocol


class UserRecord(Protocol):
    """Represent a stored user.

    Implementations must expose the user's identifier as a string,
    converting it from the underlying database type if necessary.
    """

    @property
    def id(self) -> str:
        """Return the user's unique identifier."""
        ...

    @property
    def username(self) -> str:
        """Return the user's username."""
        ...

    @property
    def hashed_password(self) -> str:
        """Return the user's hashed password."""
        ...


class UserStore(Protocol):
    """Define a backend that looks up stored users."""

    def get_by_username(self, username: str) -> UserRecord | None:
        """Return the user with the given username, or None if not found."""
        ...


class SessionRecord(Protocol):
    """Represent a stored session.

    Implementations store only a hash of the token,
    never the token itself.
    """

    @property
    def token_hash(self) -> str:
        """Return the SHA-256 hash of the session token."""
        ...

    @property
    def user_id(self) -> str:
        """Return the user's unique identifier."""
        ...

    @property
    def username(self) -> str:
        """Return the user's username."""
        ...

    @property
    def created_at(self) -> datetime:
        """Return when the session was created, in UTC."""
        ...

    @property
    def expires_at(self) -> datetime:
        """Return when the session expires, in UTC."""
        ...


class SessionStore(Protocol):
    """Define a backend that stores sessions.

    Methods receive token hashes, never raw tokens.
    """

    def add(self, session: SessionRecord) -> None:
        """Store a new session."""
        ...

    def get_by_token_hash(self, token_hash: str) -> SessionRecord | None:
        """Return the session with the given token hash, or None if not found."""
        ...

    def delete(self, token_hash: str) -> None:
        """Delete the session with the given token hash, if it exists."""
        ...


class RoleAssignmentStore(Protocol):
    """Define a backend that records which roles are assigned to each user.

    Roles themselves are defined in code. The store only keeps role names.
    """

    def get_roles(self, user_id: str) -> frozenset[str]:
        """Return the names of the roles assigned to the user.

        Return an empty set if the user has no roles.
        """
        ...
