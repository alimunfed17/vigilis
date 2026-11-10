"""Provide in-memory user and session stores."""

from dataclasses import dataclass
from datetime import datetime

from masoon.errors import UserAlreadyExistsError
from masoon.storage.protocols import SessionRecord


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


@dataclass(frozen=True, slots=True)
class StoredSession:
    """Represent a session stored by an in-memory session store."""

    token_hash: str
    user_id: str
    username: str
    created_at: datetime
    expires_at: datetime


class InMemorySessionStore:
    """Store sessions in memory, indexed by token hash."""

    def __init__(self) -> None:
        """Initialize an empty session store."""
        self._sessions: dict[str, SessionRecord] = {}

    def add(self, session: SessionRecord) -> None:
        """Store a session, indexed by its token hash."""
        self._sessions[session.token_hash] = session

    def get_by_token_hash(self, token_hash: str) -> SessionRecord | None:
        """Return the session with the given token hash, or None if not found."""
        return self._sessions.get(token_hash)

    def delete(self, token_hash: str) -> None:
        """Delete a session if it exists."""
        self._sessions.pop(token_hash, None)
