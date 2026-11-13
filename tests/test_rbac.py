import pytest

from masoon.authz.rbac import Authorizer
from masoon.errors import PermissionDeniedError
from masoon.storage.memory import InMemoryRoleAssignmentStore
from masoon.types import Identity, Role

VIEWER = Role(name="viewer", permissions=frozenset({"posts:read"}))
EDITOR = Role(name="editor", permissions=frozenset({"posts:read", "posts:edit"}))
MODERATOR = Role(name="moderator", permissions=frozenset({"comments:delete"}))

ALICE = Identity(id="1", username="alice")


@pytest.fixture
def assignments() -> InMemoryRoleAssignmentStore:
    return InMemoryRoleAssignmentStore()


@pytest.fixture
def authorizer(assignments: InMemoryRoleAssignmentStore) -> Authorizer:
    return Authorizer(roles=[VIEWER, EDITOR, MODERATOR], assignments=assignments)


def test_role_grants_permission(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
) -> None:
    assignments.assign(ALICE.id, "editor")

    assert authorizer.has_permission(ALICE, "posts:edit") is True


def test_role_without_permission_is_denied(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
) -> None:
    assignments.assign(ALICE.id, "viewer")

    assert authorizer.has_permission(ALICE, "posts:edit") is False


def test_require_raises_when_denied(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
) -> None:
    assignments.assign(ALICE.id, "viewer")

    with pytest.raises(PermissionDeniedError, match="posts:edit"):
        authorizer.require(ALICE, "posts:edit")


def test_require_passes_when_allowed(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
) -> None:
    assignments.assign(ALICE.id, "editor")

    authorizer.require(ALICE, "posts:edit")


def test_user_without_roles_is_denied(authorizer: Authorizer) -> None:
    assert authorizer.has_permission(ALICE, "posts:read") is False
    assert authorizer.permissions_for(ALICE) == frozenset()


def test_undefined_role_grants_nothing(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
) -> None:
    assignments.assign(ALICE.id, "admin")

    assert authorizer.has_permission(ALICE, "posts:read") is False
    assert authorizer.permissions_for(ALICE) == frozenset()


def test_permissions_from_several_roles_combine(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
) -> None:
    assignments.assign(ALICE.id, "viewer")
    assignments.assign(ALICE.id, "moderator")

    assert authorizer.permissions_for(ALICE) == frozenset({"posts:read", "comments:delete"})


@pytest.mark.parametrize("permission", ["Posts:Edit", "posts:*", "posts", "posts:edit "])
def test_permissions_match_exactly(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
    permission: str,
) -> None:
    assignments.assign(ALICE.id, "editor")

    assert authorizer.has_permission(ALICE, permission) is False


def test_unassigning_role_removes_permissions(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
) -> None:
    assignments.assign(ALICE.id, "editor")
    assignments.unassign(ALICE.id, "editor")

    assert authorizer.has_permission(ALICE, "posts:edit") is False


def test_permissions_are_per_user(
    authorizer: Authorizer,
    assignments: InMemoryRoleAssignmentStore,
) -> None:
    assignments.assign(ALICE.id, "editor")
    bob = Identity(id="2", username="bob")

    assert authorizer.has_permission(bob, "posts:edit") is False


def test_duplicate_role_names_raise(assignments: InMemoryRoleAssignmentStore) -> None:
    duplicate = Role(name="viewer", permissions=frozenset({"posts:edit"}))

    with pytest.raises(ValueError, match="Duplicate role name: viewer"):
        Authorizer(roles=[VIEWER, duplicate], assignments=assignments)


def test_roles_can_be_any_iterable(assignments: InMemoryRoleAssignmentStore) -> None:
    assignments.assign(ALICE.id, "viewer")
    authorizer = Authorizer(roles=(role for role in [VIEWER]), assignments=assignments)

    assert authorizer.has_permission(ALICE, "posts:read") is True
