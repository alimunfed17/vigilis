"""Masoon: framework-agnostic authN and authZ for Python."""

from typing import TYPE_CHECKING

from masoon.authn.authenticator import Authenticator
from masoon.authn.passwords import PasswordHasher
from masoon.authn.sessions import SessionManager
from masoon.authz.rbac import Authorizer
from masoon.errors import (
    AuthenticationError,
    AuthorizationError,
    InvalidCredentialsError,
    InvalidSessionError,
    MasoonError,
    PermissionDeniedError,
    UserAlreadyExistsError,
)
from masoon.storage.memory import (
    InMemoryRoleAssignmentStore,
    InMemorySessionStore,
    InMemoryUserStore,
    StoredSession,
    StoredUser,
)
from masoon.storage.protocols import (
    RoleAssignmentStore,
    SessionRecord,
    SessionStore,
    UserRecord,
    UserStore,
)
from masoon.types import Identity, Role

if TYPE_CHECKING:
    from masoon.authn.argon2_hasher import Argon2PasswordHasher

__all__ = [
    "Argon2PasswordHasher",
    "AuthenticationError",
    "Authenticator",
    "AuthorizationError",
    "Authorizer",
    "Identity",
    "InMemoryRoleAssignmentStore",
    "InMemorySessionStore",
    "InMemoryUserStore",
    "InvalidCredentialsError",
    "InvalidSessionError",
    "MasoonError",
    "PasswordHasher",
    "PermissionDeniedError",
    "Role",
    "RoleAssignmentStore",
    "SessionManager",
    "SessionRecord",
    "SessionStore",
    "StoredSession",
    "StoredUser",
    "UserAlreadyExistsError",
    "UserRecord",
    "UserStore",
]


def __getattr__(name: str) -> object:
    """Import optional components only when they are first accessed.

    ``Argon2PasswordHasher`` needs the optional ``argon2`` extra, so it is
    imported lazily. This keeps ``import masoon`` working without the extra.
    """
    if name == "Argon2PasswordHasher":
        try:
            from masoon.authn.argon2_hasher import Argon2PasswordHasher  # noqa: PLC0415
        except ModuleNotFoundError as error:
            msg = (
                "Argon2PasswordHasher requires the 'argon2' extra. "
                "Install it with: pip install 'masoon[argon2]'"
            )
            raise ImportError(msg) from error
        return Argon2PasswordHasher

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
