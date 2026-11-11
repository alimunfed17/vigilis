"""Create, validate, and revoke session tokens."""

import hashlib
import secrets
from collections.abc import Callable
from datetime import UTC, datetime, timedelta

from masoon.errors import InvalidSessionError
from masoon.storage.memory import StoredSession
from masoon.storage.protocols import SessionStore
from masoon.types import Identity


def _utc_now() -> datetime:
    return datetime.now(UTC)


def _generate_token() -> str:
    return secrets.token_urlsafe(32)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


class SessionManager:
    """Manage session tokens for authenticated users.

    Tokens are random and returned only once, when the session is created.
    Only a SHA-256 hash of each token is stored.
    """

    def __init__(
        self,
        store: SessionStore,
        validity: timedelta,
        *,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        """Initialize the session manager.

        Args:
            store: The session store that keeps session records.
            validity: How long a session stays valid after it is created.
            clock: A function that returns the current time in UTC. Defaults to the
                system clock. Pass a custom clock in tests to control time.

        Raises:
            ValueError: If the validity is zero or negative.

        """
        if validity <= timedelta(0):
            msg = "Session validity must be positive."
            raise ValueError(msg)

        self._store = store
        self._validity = validity
        self._clock = clock if clock is not None else _utc_now

    def create(self, identity: Identity) -> str:
        """Create a session for the identity and return its token.

        The token is returned only here. Store it on the client, for example in a
        cookie, because it cannot be recovered later.
        """
        now = self._clock()
        token = _generate_token()

        session = StoredSession(
            token_hash=_hash_token(token),
            user_id=identity.id,
            username=identity.username,
            created_at=now,
            expires_at=now + self._validity,
        )
        self._store.add(session)

        return token

    def validate(self, token: str) -> Identity:
        """Return the identity for a valid session token.

        Expired sessions are deleted from the store.

        Raises:
            InvalidSessionError: If the token is unknown, expired, or revoked.

        """
        token_hash = _hash_token(token)
        session = self._store.get_by_token_hash(token_hash)

        if session is None:
            raise InvalidSessionError

        if self._clock() >= session.expires_at:
            self._store.delete(token_hash)
            raise InvalidSessionError

        return Identity(id=session.user_id, username=session.username)

    def revoke(self, token: str) -> None:
        """Revoke a session token. Revoking an unknown token does nothing."""
        self._store.delete(_hash_token(token))
