from dataclasses import FrozenInstanceError

import pytest

from masoon.types import Role


def test_role_fields() -> None:
    role = Role(name="editor", permissions=frozenset({"posts:read", "posts:edit"}))

    assert role.name == "editor"
    assert role.permissions == frozenset({"posts:read", "posts:edit"})


def test_role_is_frozen() -> None:
    role = Role(name="editor", permissions=frozenset({"posts:read"}))

    with pytest.raises(FrozenInstanceError):
        role.name = "admin"  # ty: ignore[invalid-assignment]
