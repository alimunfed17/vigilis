"""Define shared types used throughout Vigilis."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Identity:
    """Represent the identity of an authenticated user."""

    id: str
    username: str
