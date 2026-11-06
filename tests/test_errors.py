from vigilis.errors import (
    AuthenticationError,
    InvalidCredentialsError,
    UserAlreadyExistsError,
    VigilisError,
)


def test_invalid_credentials_error_inheritance() -> None:
    assert issubclass(InvalidCredentialsError, AuthenticationError)
    assert issubclass(InvalidCredentialsError, VigilisError)


def test_invalid_credentials_error_message() -> None:
    error = InvalidCredentialsError("Invalid credentials")

    assert str(error) == "Invalid credentials"
    assert isinstance(error, AuthenticationError)
    assert isinstance(error, VigilisError)


def test_user_already_exists_error_inheritance() -> None:
    assert issubclass(UserAlreadyExistsError, VigilisError)


def test_user_already_exists_error() -> None:
    error = UserAlreadyExistsError("apple")

    assert str(error) == "User 'apple' already exists."
    assert error.username == "apple"
    assert isinstance(error, VigilisError)
