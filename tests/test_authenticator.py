import pytest

from vigilis.authn.argon2_hasher import Argon2PasswordHasher
from vigilis.authn.authenticator import Authenticator
from vigilis.errors import InvalidCredentialsError
from vigilis.storage.memory import InMemoryUserStore, StoredUser
from vigilis.types import Identity


class CountingHasher:
    """Wrap a real hasher and count how often passwords are verified."""

    def __init__(self) -> None:
        self._hasher = Argon2PasswordHasher()
        self.verify_calls = 0

    def hash_password(self, password: str) -> str:
        return self._hasher.hash_password(password=password)

    def verify_password(self, password: str, hashed_password: str) -> bool:
        self.verify_calls += 1
        return self._hasher.verify_password(password=password, hashed_password=hashed_password)


@pytest.fixture
def authenticator() -> Authenticator:
    hasher = Argon2PasswordHasher()

    store = InMemoryUserStore()
    store.add(
        StoredUser(
            id="1",
            username="apple",
            hashed_password=hasher.hash_password(password="password_1"),
        ),
    )

    return Authenticator(store=store, hasher=hasher)


def test_correct_password(authenticator: Authenticator) -> None:
    identity = authenticator.authenticate(username="apple", password="password_1")

    assert identity == Identity(id="1", username="apple")


def test_wrong_password(authenticator: Authenticator) -> None:
    with pytest.raises(InvalidCredentialsError):
        authenticator.authenticate(username="apple", password="password_2")


def test_unknown_user(authenticator: Authenticator) -> None:
    with pytest.raises(InvalidCredentialsError):
        authenticator.authenticate(username="unknown", password="password_1")


def test_wrong_password_and_unknown_user_have_same_error(authenticator: Authenticator) -> None:
    with pytest.raises(InvalidCredentialsError) as wrong_password:
        authenticator.authenticate(username="apple", password="wrong_password")

    with pytest.raises(InvalidCredentialsError) as unknown_user:
        authenticator.authenticate(username="unknown", password="password_1")

    assert str(wrong_password.value) == str(unknown_user.value)


def test_unknown_user_still_verifies_a_password() -> None:
    hasher = CountingHasher()
    authenticator = Authenticator(store=InMemoryUserStore(), hasher=hasher)

    with pytest.raises(InvalidCredentialsError):
        authenticator.authenticate(username="unknown", password="password_1")

    assert hasher.verify_calls == 1
