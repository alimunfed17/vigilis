from vigilis.errors import AuthenticationError, InvalidCredentialsError, VigilisError


def test_invalid_credentials_error_inheritance() -> None:
    assert issubclass(InvalidCredentialsError, AuthenticationError)
    assert issubclass(InvalidCredentialsError, VigilisError)


def test_invalid_credentials_error_message() -> None:
    error = InvalidCredentialsError("Invalid credentials")

    assert str(error) == "Invalid credentials"
    assert isinstance(error, AuthenticationError)
    assert isinstance(error, VigilisError)
