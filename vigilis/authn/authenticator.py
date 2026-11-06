"""Authenticate users with a username and password."""

import secrets

from vigilis.authn.passwords import PasswordHasher
from vigilis.errors import InvalidCredentialsError
from vigilis.storage.protocols import UserStore
from vigilis.types import Identity


class Authenticator:
    """Verify a username and password against a user store."""

    def __init__(self, store: UserStore, hasher: PasswordHasher) -> None:
        """Initialize the authenticator with a user store and a password hasher.

        A dummy hash of a random value is created once, so that logins for
        unknown usernames take about as long as logins with a wrong password.
        """
        self._store = store
        self._hasher = hasher
        self._dummy_hash = hasher.hash_password(password=secrets.token_urlsafe(32))

    def authenticate(self, username: str, password: str) -> Identity:
        """Return the identity of the user if the credentials are valid.

        Raises:
            InvalidCredentialsError: If the username does not exist or the
                password is wrong. Both cases raise the same error.

        """
        user = self._store.get_by_username(username)

        if user is None:
            self._hasher.verify_password(password=password, hashed_password=self._dummy_hash)
            raise InvalidCredentialsError

        is_valid = self._hasher.verify_password(
            password=password,
            hashed_password=user.hashed_password,
        )
        if not is_valid:
            raise InvalidCredentialsError

        return Identity(id=user.id, username=user.username)
