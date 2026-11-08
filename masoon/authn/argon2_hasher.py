"""Provide a password hasher backed by Argon2.

Requires the optional ``argon2`` extra: ``pip install masoon[argon2]``.
"""

from argon2 import PasswordHasher as Argon2Hasher
from argon2.exceptions import VerifyMismatchError


class Argon2PasswordHasher:
    """Hash and verify passwords with Argon2 using the library's secure defaults."""

    def __init__(self) -> None:
        """Initialize the hasher with Argon2's default parameters."""
        self._hasher = Argon2Hasher()

    def hash_password(self, password: str) -> str:
        """Return an Argon2 hash of the given password."""
        return self._hasher.hash(password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Return whether the password matches the hashed password.

        Raises:
            argon2.exceptions.InvalidHashError: If the hashed password is malformed.

        """
        try:
            self._hasher.verify(hashed_password, password)
        except VerifyMismatchError:
            return False

        return True
