from dataclasses import FrozenInstanceError

import pytest

from vigilis.types import Identity


def test_identity_fields() -> None:
    identity = Identity(id="1", username="apple")

    assert identity.id == "1"
    assert identity.username == "apple"


def test_identity_is_frozen() -> None:
    identity = Identity(id="1", username="apple")

    with pytest.raises(FrozenInstanceError):
        identity.username = "orange"  # ty: ignore[invalid-assignment]
