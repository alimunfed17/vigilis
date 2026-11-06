"""Define the protocol that password hashers must implement."""

from typing import Protocol


class PasswordHasher(Protocol):
    """Hash passwords and verify passwords against stored hashes."""

    def hash_password(self, password: str) -> str:
        """Return a hash of the given password."""
        ...

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Return whether the password matches the hashed password."""
        ...
