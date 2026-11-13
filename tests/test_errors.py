from masoon.errors import (
    AuthenticationError,
    AuthorizationError,
    InvalidCredentialsError,
    InvalidSessionError,
    MasoonError,
    PermissionDeniedError,
    UserAlreadyExistsError,
)


def test_invalid_credentials_error_inheritance() -> None:
    assert issubclass(InvalidCredentialsError, AuthenticationError)
    assert issubclass(InvalidCredentialsError, MasoonError)


def test_invalid_credentials_error_message() -> None:
    error = InvalidCredentialsError("Invalid credentials")

    assert str(error) == "Invalid credentials"
    assert isinstance(error, AuthenticationError)
    assert isinstance(error, MasoonError)


def test_user_already_exists_error_inheritance() -> None:
    assert issubclass(UserAlreadyExistsError, MasoonError)


def test_user_already_exists_error() -> None:
    error = UserAlreadyExistsError("apple")

    assert str(error) == "User 'apple' already exists."
    assert error.username == "apple"
    assert isinstance(error, MasoonError)


def test_invalid_session_error_inheritance() -> None:
    assert issubclass(InvalidSessionError, AuthenticationError)
    assert issubclass(InvalidSessionError, MasoonError)


def test_invalid_session_error() -> None:
    error = InvalidSessionError()

    assert str(error) == "Invalid session."
    assert isinstance(error, AuthenticationError)
    assert isinstance(error, MasoonError)


def test_authorization_error_is_not_an_authentication_error() -> None:
    assert issubclass(AuthorizationError, MasoonError)
    assert not issubclass(AuthorizationError, AuthenticationError)


def test_permission_denied_error() -> None:
    error = PermissionDeniedError("posts:edit")

    assert str(error) == "Permission denied: posts:edit"
    assert error.permission_name == "posts:edit"
    assert isinstance(error, AuthorizationError)
    assert isinstance(error, MasoonError)
