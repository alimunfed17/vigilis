# Vigilis

Framework-agnostic authentication and authorization for Python.

> **Status: pre-alpha.** Vigilis is in early development. The API will change
> and it is not ready for production use.

## Features

**Available now**

- **Username and password login** with a single `Authenticator`.
- **Argon2 password hashing** with secure defaults (optional extra).
- **Bring your own storage**: plug in any database or ORM by implementing a small protocol.
- **Safe failures**: a wrong password and an unknown username raise the same error and take
  about the same time, so attackers cannot discover which usernames exist.
- **Typed**: fully type-hinted and checked with ty.
- **Minimal core**: no required dependencies.

**Planned**

- Tokens and sessions.
- Authorization: composable policies and role-based access control.
- Integrations for FastAPI, Django, and Flask.

## Installation

Vigilis requires Python 3.12 or newer. Install it with the `argon2` extra to get the
built-in password hasher:

```bash
pip install 'vigilis[argon2]'
```

Or with uv:

```bash
uv add 'vigilis[argon2]'
```

Installing plain `vigilis` gives you the core only. You then need to provide your own
password hasher.

## Quick start

```python
from vigilis import (
    Argon2PasswordHasher,
    Authenticator,
    InMemoryUserStore,
    InvalidCredentialsError,
    StoredUser,
)

hasher = Argon2PasswordHasher()

# Register a user. Always store the hash, never the password itself.
store = InMemoryUserStore()
store.add(
    StoredUser(
        id="1",
        username="alice",
        hashed_password=hasher.hash_password(password="correct horse battery staple"),
    ),
)

authenticator = Authenticator(store=store, hasher=hasher)

# A successful login returns the user's identity.
identity = authenticator.authenticate(
    username="alice",
    password="correct horse battery staple",
)
print(identity)  # Identity(id='1', username='alice')

# A failed login raises InvalidCredentialsError.
try:
    authenticator.authenticate(username="alice", password="wrong password")
except InvalidCredentialsError as error:
    print(error)  # Invalid username or password.
```

`InMemoryUserStore` is meant for tests and examples. In a real application, connect your
own database as shown below.

## Using your own database

`Authenticator` accepts any object that matches the `UserStore` protocol. There is no
base class to inherit from: your store only needs a `get_by_username` method that returns
a user record, or `None` if the user does not exist.

A user record needs three readable attributes, all strings: `id`, `username`, and
`hashed_password`. If your database uses another type for IDs, such as integers, convert
them to strings in your store.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class UserRow:
    id: str
    username: str
    hashed_password: str


class DatabaseUserStore:
    def __init__(self, connection) -> None:
        self._connection = connection

    def get_by_username(self, username: str) -> UserRow | None:
        row = self._connection.execute(
            "SELECT id, username, hashed_password FROM users WHERE username = ?",
            (username,),
        ).fetchone()
        if row is None:
            return None
        return UserRow(id=str(row[0]), username=row[1], hashed_password=row[2])
```

Pass it to the authenticator like any other store:

```python
authenticator = Authenticator(store=DatabaseUserStore(connection), hasher=hasher)
```

## Errors

All exceptions raised by Vigilis inherit from `VigilisError`.

| Exception | Raised when |
|---|---|
| `InvalidCredentialsError` | The username does not exist or the password is wrong. |
| `UserAlreadyExistsError` | A user is added to `InMemoryUserStore` with a username that is already taken. |
| `AuthenticationError` | Base class for all authentication errors. |
| `VigilisError` | Base class for every Vigilis error. |

## License

Licensed under the [Apache License 2.0](LICENSE).
