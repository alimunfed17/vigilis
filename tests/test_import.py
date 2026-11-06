import importlib
import sys

import pytest

import vigilis


def test_all_public_names_are_available() -> None:
    for name in vigilis.__all__:
        assert hasattr(vigilis, name), name


def test_argon2_hasher_is_available_from_package() -> None:
    from vigilis import Argon2PasswordHasher  # noqa: PLC0415
    from vigilis.authn.argon2_hasher import (  # noqa: PLC0415
        Argon2PasswordHasher as Argon2PasswordHasherFromModule,
    )

    assert Argon2PasswordHasher is Argon2PasswordHasherFromModule


def test_unknown_attribute_raises_attribute_error() -> None:
    with pytest.raises(AttributeError):
        _ = vigilis.DoesNotExist


def _hide_argon2(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make Python behave as if argon2 is not installed and reload vigilis."""
    monkeypatch.setitem(sys.modules, "argon2", None)
    for module_name in list(sys.modules):
        if module_name == "vigilis" or module_name.startswith(("vigilis.", "argon2.")):
            monkeypatch.delitem(sys.modules, module_name)


def test_import_works_without_argon2(monkeypatch: pytest.MonkeyPatch) -> None:
    _hide_argon2(monkeypatch)

    package = importlib.import_module("vigilis")

    assert package.Authenticator is not None


def test_argon2_hasher_without_extra_gives_helpful_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _hide_argon2(monkeypatch)
    package = importlib.import_module("vigilis")

    with pytest.raises(ImportError, match=r"vigilis\[argon2\]"):
        _ = package.Argon2PasswordHasher
