"""Define exceptions raised by Vigilis."""


class VigilisError(Exception):
    """Base exception for all Vigilis-related errors."""


class AuthenticationError(VigilisError):
    """Base exception for authentication-related errors."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided credentials are invalid.

    The default message is deliberately generic so it never reveals whether
    the username or the password was wrong.
    """

    def __init__(self, message: str = "Invalid username or password.") -> None:
        """Initialize the exception with an optional custom message."""
        super().__init__(message)


class UserAlreadyExistsError(VigilisError):
    """Raised when a user with the given username already exists."""

    def __init__(self, username: str) -> None:
        """Initialize the exception with the conflicting username."""
        self.username = username
        super().__init__(f"User '{username}' already exists.")
