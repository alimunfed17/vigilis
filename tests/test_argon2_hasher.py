from typing import TYPE_CHECKING

import pytest
from argon2.exceptions import InvalidHashError

from masoon.authn.argon2_hasher import Argon2PasswordHasher

if TYPE_CHECKING:
    from masoon.authn.passwords import PasswordHasher


def test_correct_password() -> None:
    hasher = Argon2PasswordHasher()

    password = "secure-password"
    hashed_password = hasher.hash_password(password=password)

    assert hasher.verify_password(password=password, hashed_password=hashed_password) is True


def test_wrong_password() -> None:
    hasher = Argon2PasswordHasher()

    password = "secure-password"
    hashed_password = hasher.hash_password(password=password)

    assert (
        hasher.verify_password(password="secure-2-password", hashed_password=hashed_password)
        is False
    )


def test_hash_not_password() -> None:
    hasher = Argon2PasswordHasher()

    password = "secure-password"
    hashed_password = hasher.hash_password(password=password)

    assert password != hashed_password


def test_hashes_differ() -> None:
    hasher = Argon2PasswordHasher()

    password = "secure-password"
    first_hash = hasher.hash_password(password=password)
    second_hash = hasher.hash_password(password=password)

    assert first_hash != second_hash


def test_malformed_hash_raises() -> None:
    hasher = Argon2PasswordHasher()

    with pytest.raises(InvalidHashError):
        hasher.verify_password(password="secure-password", hashed_password="invalid-hash")


def test_argon2_hasher_implements_password_hasher_protocol() -> None:
    hasher: PasswordHasher = Argon2PasswordHasher()

    hashed_password = hasher.hash_password(password="secure-password")

    assert hasher.verify_password(password="secure-password", hashed_password=hashed_password)
