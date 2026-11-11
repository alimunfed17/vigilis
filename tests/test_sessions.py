import hashlib
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import pytest

from masoon.authn.sessions import SessionManager
from masoon.errors import InvalidSessionError
from masoon.storage.memory import InMemorySessionStore
from masoon.types import Identity


class FakeTime:
    def __init__(self) -> None:
        self.now = datetime(2026, 11, 11, tzinfo=UTC)

    def __call__(self) -> datetime:
        return self.now


@dataclass(frozen=True)
class SessionFixture:
    manager: SessionManager
    clock: FakeTime
    store: InMemorySessionStore
    token: str
    identity: Identity


@pytest.fixture
def create_session() -> SessionFixture:
    clock = FakeTime()
    store = InMemorySessionStore()
    manager = SessionManager(
        store=store,
        validity=timedelta(days=1),
        clock=clock,
    )
    identity = Identity(id="1", username="apple")
    token = manager.create(identity)

    return SessionFixture(
        manager=manager,
        clock=clock,
        store=store,
        token=token,
        identity=identity,
    )


def test_create_and_validate_session(create_session: SessionFixture) -> None:
    assert create_session.manager.validate(create_session.token) == create_session.identity


def test_unknown_token(create_session: SessionFixture) -> None:
    with pytest.raises(InvalidSessionError):
        create_session.manager.validate("unknown-token")


def test_expired_session(create_session: SessionFixture) -> None:
    create_session.clock.now += timedelta(days=2)

    with pytest.raises(InvalidSessionError):
        create_session.manager.validate(create_session.token)


def test_expires_now(create_session: SessionFixture) -> None:
    create_session.clock.now += timedelta(days=1)

    with pytest.raises(InvalidSessionError):
        create_session.manager.validate(create_session.token)


def test_valid_before_expiry(create_session: SessionFixture) -> None:
    create_session.clock.now += timedelta(days=1) - timedelta(minutes=5)

    assert create_session.manager.validate(create_session.token) == create_session.identity


def test_remove_expired_session(create_session: SessionFixture) -> None:
    create_session.clock.now += timedelta(days=2)

    with pytest.raises(InvalidSessionError):
        create_session.manager.validate(create_session.token)

    token_hash = hashlib.sha256(create_session.token.encode("utf-8")).hexdigest()

    assert create_session.store.get_by_token_hash(token_hash) is None


def test_revoked_token_raises(create_session: SessionFixture) -> None:
    create_session.manager.revoke(create_session.token)

    with pytest.raises(InvalidSessionError):
        create_session.manager.validate(create_session.token)


def test_revoking_an_unknown_token(create_session: SessionFixture) -> None:
    create_session.manager.revoke("unknown-token")

    assert create_session.manager.validate(create_session.token) == create_session.identity


def test_two_create_calls_give_different_tokens(
    create_session: SessionFixture,
) -> None:
    second_token = create_session.manager.create(create_session.identity)

    assert create_session.token != second_token


def test_only_hashed_token_is_stored(create_session: SessionFixture) -> None:
    expected_hash = hashlib.sha256(create_session.token.encode("utf-8")).hexdigest()

    assert create_session.store.get_by_token_hash(create_session.token) is None
    assert create_session.store.get_by_token_hash(expected_hash) is not None


@pytest.mark.parametrize(
    "validity",
    [
        timedelta(0),
        timedelta(days=-1),
    ],
)
def test_invalid_validity(validity: timedelta) -> None:
    store = InMemorySessionStore()

    with pytest.raises(
        ValueError,
        match="Session validity must be positive",
    ):
        SessionManager(
            store=store,
            validity=validity,
        )
