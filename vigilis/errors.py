"""Define exceptions raised by Vigilis."""


class VigilisError(Exception):
    """Base exception for all Vigilis-related errors."""


class AuthenticationError(VigilisError):
    """Base exception for authentication-related errors."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided credentials are invalid."""


class UserAlreadyExistsError(VigilisError):
    """Raised when a user with the given username already exists."""

    def __init__(self, username: str) -> None:
        """Initialize the exception with the conflicting username."""
        self.username = username
        super().__init__(f"User '{username}' already exists.")
