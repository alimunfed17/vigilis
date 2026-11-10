from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest

from masoon.errors import UserAlreadyExistsError
from masoon.storage.memory import (
    InMemorySessionStore,
    InMemoryUserStore,
    StoredSession,
    StoredUser,
)

if TYPE_CHECKING:
    from masoon.storage.protocols import SessionRecord, SessionStore, UserStore


@pytest.fixture
def session() -> StoredSession:
    return StoredSession(
        token_hash="fake-token-hash",
        user_id="1",
        username="apple",
        created_at=datetime(2026, 11, 10, tzinfo=UTC),
        expires_at=datetime(2026, 11, 12, tzinfo=UTC),
    )


def test_add_and_get_user() -> None:
    user = StoredUser(
        id="1",
        username="apple",
        hashed_password="fake-hash",
    )

    store = InMemoryUserStore()
    store.add(user)

    assert store.get_by_username("apple") == user


def test_unknown_user_returns_none() -> None:
    store = InMemoryUserStore()

    assert store.get_by_username("apple") is None


def test_add_duplicate_username_raises() -> None:
    user_1 = StoredUser(
        id="1",
        username="apple",
        hashed_password="fake-hash",
    )
    user_2 = StoredUser(
        id="2",
        username="apple",
        hashed_password="another-fake-hash",
    )

    store = InMemoryUserStore()
    store.add(user_1)

    with pytest.raises(UserAlreadyExistsError):
        store.add(user_2)


def test_in_memory_store_implements_user_store_protocol() -> None:
    store: UserStore = InMemoryUserStore()

    assert store.get_by_username("apple") is None


def test_add_and_get_session(session: StoredSession) -> None:
    store = InMemorySessionStore()
    store.add(session)

    assert store.get_by_token_hash(session.token_hash) == session


def test_unknown_session_returns_none() -> None:
    store = InMemorySessionStore()

    assert store.get_by_token_hash("unknown-hash") is None


def test_delete_session(session: StoredSession) -> None:
    store = InMemorySessionStore()
    store.add(session)

    store.delete(session.token_hash)

    assert store.get_by_token_hash(session.token_hash) is None


def test_delete_unknown_session_does_not_raise() -> None:
    store = InMemorySessionStore()

    store.delete("unknown-hash")


def test_in_memory_session_store_implements_session_store_protocol() -> None:
    store: SessionStore = InMemorySessionStore()

    assert store.get_by_token_hash("unknown-hash") is None


def test_stored_session_implements_session_record_protocol(
    session: StoredSession,
) -> None:
    record: SessionRecord = session

    assert record.username == "apple"
