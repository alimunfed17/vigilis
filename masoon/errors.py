"""Define exceptions raised by Masoon."""


class MasoonError(Exception):
    """Base exception for all Masoon-related errors."""


class AuthenticationError(MasoonError):
    """Base exception for authentication-related errors."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided credentials are invalid.

    The default message is deliberately generic so it never reveals whether
    the username or the password was wrong.
    """

    def __init__(self, message: str = "Invalid username or password.") -> None:
        """Initialize the exception with an optional custom message."""
        super().__init__(message)


class InvalidSessionError(AuthenticationError):
    """Raised when a session token is invalid, expired, or revoked.

    The default message is deliberately generic to avoid revealing why
    a session token was rejected.
    """

    def __init__(self, message: str = "Invalid session.") -> None:
        """Initialize the exception with an optional custom message."""
        super().__init__(message)


class UserAlreadyExistsError(MasoonError):
    """Raised when a user with the given username already exists."""

    def __init__(self, username: str) -> None:
        """Initialize the exception with the conflicting username."""
        self.username = username
        super().__init__(f"User '{username}' already exists.")
