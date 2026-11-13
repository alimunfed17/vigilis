# Masoon

Framework-agnostic authentication and authorization for Python.

> **Status: pre-alpha.** Masoon is in early development. The API will change
> and it is not ready for production use.

## Features

**Available now**

- **Username and password login** with a single `Authenticator`.
- **Session tokens**: keep users logged in, with expiry and logout. Only a hash of each
  token is stored.
- **Role-based access control**: define roles in code, assign them to users, and check
  permissions. Access is denied by default.
- **Argon2 password hashing** with secure defaults (optional extra).
- **Bring your own storage**: plug in any database or ORM by implementing a small protocol.
- **Safe failures**: a wrong password and an unknown username raise the same error and take
  about the same time, so attackers cannot discover which usernames exist.
- **Typed**: fully type-hinted and checked with ty.
- **Minimal core**: no required dependencies.

**Planned**

- Composable authorization policies.
- Integrations for FastAPI, Django, and Flask.

## Installation

Masoon requires Python 3.12 or newer. Install it with the `argon2` extra to get the
built-in password hasher:

```bash
pip install 'masoon[argon2]'
```

Or with uv:

```bash
uv add 'masoon[argon2]'
```

Installing plain `masoon` gives you the core only. You then need to provide your own
password hasher.

## Quick start

```python
from masoon import (
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

## Sessions

After a successful login, create a session so the user stays logged in. `SessionManager`
returns a random token that your application sends to the client, for example in a
cookie. On later requests, validate the token to get the user's identity back.

```python
from datetime import timedelta

from masoon import InMemorySessionStore, InvalidSessionError, SessionManager

sessions = SessionManager(store=InMemorySessionStore(), validity=timedelta(days=1))

# Log in, then create a session for the identity.
token = sessions.create(identity)

# On each later request, validate the token sent by the client.
identity = sessions.validate(token)
print(identity)  # Identity(id='1', username='alice')

# On logout, revoke the session. The token stops working immediately.
sessions.revoke(token)

try:
    sessions.validate(token)
except InvalidSessionError as error:
    print(error)  # Invalid session.
```

How sessions work:

- **The token is returned only once**, by `create`. Masoon stores a SHA-256 hash of it,
  never the token itself, so a leaked session database cannot be used to log in.
- **Sessions expire** after the `validity` you choose. Validating an expired token raises
  `InvalidSessionError` and removes the session from the store.
- **One error for every failure.** Unknown, expired, and revoked tokens all raise the same
  `InvalidSessionError`, so the error never reveals why a token was rejected.
- **Revoking is safe to repeat.** Revoking a token that does not exist does nothing.

`InMemorySessionStore` loses all sessions when your application restarts. In a real
application, store sessions in your own database as shown below.

## Authorization

Masoon uses role-based access control. Define roles in your code, each with a set of
permissions, then record which roles each user has. `Authorizer` answers whether an
identity is allowed to do something.

```python
from masoon import (
    Authorizer,
    Identity,
    InMemoryRoleAssignmentStore,
    PermissionDeniedError,
    Role,
)

# Define roles in code. Permissions are plain strings.
viewer = Role(name="viewer", permissions=frozenset({"posts:read"}))
editor = Role(name="editor", permissions=frozenset({"posts:read", "posts:edit"}))

# Record which roles each user has.
assignments = InMemoryRoleAssignmentStore()
assignments.assign(user_id="1", role_name="editor")

authorizer = Authorizer(roles=[viewer, editor], assignments=assignments)
alice = Identity(id="1", username="alice")

print(authorizer.has_permission(alice, "posts:edit"))  # True
print(authorizer.has_permission(alice, "posts:delete"))  # False

# In a request handler, use require. It raises if the permission is missing.
try:
    authorizer.require(alice, "posts:delete")
except PermissionDeniedError as error:
    print(error)  # Permission denied: posts:delete
```

How authorization works:

- **Access is denied by default.** A user with no roles has no permissions.
- **Undefined roles grant nothing.** If a user is assigned a role name that your code does
  not define, for example one you removed, it is ignored.
- **Permissions match exactly.** `posts:edit` does not match `Posts:Edit` or `posts:*`.
- **There is no built-in admin.** To give a user every permission, define a role that
  lists them explicitly.
- **Permissions from several roles combine.** A user with two roles has the permissions
  of both.
- **Roles cannot change after they are created.** Their permissions are always stored as
  a `frozenset`, and two roles with the same name raise `ValueError`.

`InMemoryRoleAssignmentStore` is meant for tests and examples. In a real application,
store role assignments in your own database as shown below.

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

### Sessions in your own database

`SessionManager` accepts any object that matches the `SessionStore` protocol. Your store
needs three methods, all working with token hashes:

| Method | What it does |
|---|---|
| `add(session)` | Save a new session. |
| `get_by_token_hash(token_hash)` | Return the session, or `None` if it does not exist. |
| `delete(token_hash)` | Delete the session. Do nothing if it does not exist. |

A session record has five readable attributes: `token_hash`, `user_id`, and `username`
are strings, and `created_at` and `expires_at` are timezone-aware `datetime` values in UTC.
Masoon passes a `StoredSession` to `add`, which you can store as it is.

```python
from datetime import datetime

from masoon import SessionRecord, StoredSession


class DatabaseSessionStore:
    def __init__(self, connection) -> None:
        self._connection = connection

    def add(self, session: SessionRecord) -> None:
        self._connection.execute(
            "INSERT INTO sessions VALUES (?, ?, ?, ?, ?)",
            (
                session.token_hash,
                session.user_id,
                session.username,
                session.created_at.isoformat(),
                session.expires_at.isoformat(),
            ),
        )

    def get_by_token_hash(self, token_hash: str) -> SessionRecord | None:
        row = self._connection.execute(
            "SELECT token_hash, user_id, username, created_at, expires_at"
            " FROM sessions WHERE token_hash = ?",
            (token_hash,),
        ).fetchone()
        if row is None:
            return None
        return StoredSession(
            token_hash=row[0],
            user_id=row[1],
            username=row[2],
            created_at=datetime.fromisoformat(row[3]),
            expires_at=datetime.fromisoformat(row[4]),
        )

    def delete(self, token_hash: str) -> None:
        self._connection.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))
```

### Role assignments in your own database

`Authorizer` accepts any object that matches the `RoleAssignmentStore` protocol. Your
store needs one method, `get_roles(user_id)`, which returns the names of the user's roles
as a `frozenset` of strings, or an empty `frozenset` if the user has none. Roles
themselves stay in your code; the database only records role names.

```python
class DatabaseRoleAssignmentStore:
    def __init__(self, connection) -> None:
        self._connection = connection

    def get_roles(self, user_id: str) -> frozenset[str]:
        rows = self._connection.execute(
            "SELECT role_name FROM user_roles WHERE user_id = ?",
            (user_id,),
        ).fetchall()
        return frozenset(row[0] for row in rows)
```

## Errors

All exceptions raised by Masoon inherit from `MasoonError`.

| Exception | Raised when |
|---|---|
| `InvalidCredentialsError` | The username does not exist or the password is wrong. |
| `InvalidSessionError` | A session token is unknown, expired, or revoked. |
| `PermissionDeniedError` | An identity does not have a required permission. The error names the permission. |
| `UserAlreadyExistsError` | A user is added to `InMemoryUserStore` with a username that is already taken. |
| `AuthenticationError` | Base class for all authentication errors. |
| `AuthorizationError` | Base class for all authorization errors. |
| `MasoonError` | Base class for every Masoon error. |

## License

Licensed under the [Apache License 2.0](LICENSE).
