from typing import TYPE_CHECKING

import pytest

from vigilis.errors import UserAlreadyExistsError
from vigilis.storage.memory import InMemoryUserStore, StoredUser

if TYPE_CHECKING:
    from vigilis.storage.protocols import UserStore


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
