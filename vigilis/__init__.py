"""Vigilis: framework-agnostic authN and authZ for Python."""

from typing import TYPE_CHECKING

from vigilis.authn.authenticator import Authenticator
from vigilis.authn.passwords import PasswordHasher
from vigilis.errors import (
    AuthenticationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    VigilisError,
)
from vigilis.storage.memory import InMemoryUserStore, StoredUser
from vigilis.storage.protocols import UserRecord, UserStore
from vigilis.types import Identity

if TYPE_CHECKING:
    from vigilis.authn.argon2_hasher import Argon2PasswordHasher

__all__ = [
    "Argon2PasswordHasher",
    "AuthenticationError",
    "Authenticator",
    "Identity",
    "InMemoryUserStore",
    "InvalidCredentialsError",
    "PasswordHasher",
    "StoredUser",
    "UserAlreadyExistsError",
    "UserRecord",
    "UserStore",
    "VigilisError",
]


def __getattr__(name: str) -> object:
    """Import optional components only when they are first accessed.

    ``Argon2PasswordHasher`` needs the optional ``argon2`` extra, so it is
    imported lazily. This keeps ``import vigilis`` working without the extra.
    """
    if name == "Argon2PasswordHasher":
        try:
            from vigilis.authn.argon2_hasher import Argon2PasswordHasher  # noqa: PLC0415
        except ModuleNotFoundError as error:
            msg = (
                "Argon2PasswordHasher requires the 'argon2' extra. "
                "Install it with: pip install 'vigilis[argon2]'"
            )
            raise ImportError(msg) from error
        return Argon2PasswordHasher

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
