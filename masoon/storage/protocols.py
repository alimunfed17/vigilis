"""Define protocols that user storage backends must implement."""

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
