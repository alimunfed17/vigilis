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


def test_role_copies_mutable_permissions() -> None:
    permissions = {"posts:read"}
    role = Role(name="editor", permissions=permissions)  # ty: ignore[invalid-argument-type]

    permissions.add("posts:delete")

    assert role.permissions == frozenset({"posts:read"})
    assert isinstance(role.permissions, frozenset)


def test_role_rejects_single_string() -> None:
    with pytest.raises(TypeError, match="not a single string"):
        Role(name="editor", permissions="posts:edit")  # ty: ignore[invalid-argument-type]


def test_role_rejects_non_string_permissions() -> None:
    with pytest.raises(TypeError, match="must be a string"):
        Role(name="editor", permissions=frozenset({"posts:read", 1}))  # ty: ignore[invalid-argument-type]
