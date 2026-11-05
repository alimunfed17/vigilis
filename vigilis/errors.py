"""Define exceptions raised by Vigilis."""


class VigilisError(Exception):
    """Base exception for all Vigilis-related errors."""


class AuthenticationError(VigilisError):
    """Base exception for authentication-related errors."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when the provided credentials are invalid."""
