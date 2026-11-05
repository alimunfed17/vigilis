"""Provide an in-memory user store."""

from dataclasses import dataclass

from vigilis.errors import UserAlreadyExistsError


@dataclass(frozen=True, slots=True)
class StoredUser:
    """Represent a user stored by an in-memory user store."""

    id: str
    username: str
    hashed_password: str


class InMemoryUserStore:
    """Store users in memory, indexed by username."""

    def __init__(self) -> None:
        """Initialize an empty user store."""
        self._users: dict[str, StoredUser] = {}

    def get_by_username(self, username: str) -> StoredUser | None:
        """Return the user with the given username, or None if not found."""
        return self._users.get(username)

    def add(self, user: StoredUser) -> None:
        """Add a user, raising an error if the username already exists."""
        if user.username in self._users:
            raise UserAlreadyExistsError(user.username)

        self._users[user.username] = user
