# Contributing to Vigilis

Thank you for your interest in contributing to Vigilis. This guide explains how to set up
the project, the conventions the code follows, and how to submit changes.

To report a security vulnerability, do not open an issue. Follow the instructions in
[SECURITY.md](SECURITY.md) instead.

## Development setup

Vigilis uses [uv](https://docs.astral.sh/uv/) to manage dependencies and requires
Python 3.12 or newer.

```bash
git clone https://github.com/alimunfed17/vigilis.git
cd vigilis
uv sync
uv run pre-commit install
```

`uv sync` installs Vigilis and all development tools. `pre-commit install` sets up a git
hook that checks every commit.

## Checks

Every commit and pull request must pass these checks:

| Check | Tool | Command |
|---|---|---|
| Spelling | typos | `uv run typos` |
| Workflow security | zizmor | `uv run zizmor --offline .github/` |
| Formatting | ruff | `uv run ruff format --check` |
| Linting | ruff (all rules) | `uv run ruff check` |
| Type checking | ty | `uv run ty check` |
| Tests | pytest | `uv run pytest` |

The pre-commit hook runs all of them automatically. To run them on every file at once:

```bash
uv run pre-commit run --all-files
```

The checks only report problems. They never change your code. Ruff can fix many issues
for you if you run it yourself:

```bash
uv run ruff check --fix
uv run ruff format
```

Review the changes with `git diff` before committing.

The same checks run in GitHub Actions on every push and pull request.

## Workflow

1. Create a branch from `main` using a type prefix and a short, hyphenated description:

   | Prefix | Use for |
   |---|---|
   | `feat/` | New functionality |
   | `fix/` | Bug fixes |
   | `docs/` | Documentation |
   | `test/` | Tests only |
   | `chore/` | Tooling, configuration, dependencies |
   | `ci/` | GitHub Actions workflows |

   For example: `feat/session-tokens` or `fix/empty-username`.

2. Make your changes, with tests.
3. Commit using the commit message format below.
4. Push your branch and open a pull request against `main`.

## Commit messages

Start each commit message with the type in square brackets, followed by a short
description in the imperative mood:

```text
[feat] add session token support
[fix] reject empty usernames
[test] add tests for the in-memory store
[docs] explain custom user stores
```

Use the same types as the branch prefixes. Keep each commit focused on one change, and
put source changes and their tests in separate commits where that keeps the history
clearer.

## Code guidelines

- **Type every function.** All parameters and return values need type annotations.
- **Document public code.** Every public module, class, and function needs a docstring.
- **Use protocols for extension points.** Storage backends and password hashers are
  described with `typing.Protocol`, so users can plug in their own implementations without
  inheriting from Vigilis classes.
- **Keep the core dependency-free.** Anything that needs a third-party package goes behind
  an optional extra and must not be imported by `import vigilis`.
- **Use keyword arguments** when calling functions that take several values of the same
  type, such as `verify_password(password=..., hashed_password=...)`.
- **Raise specific exceptions** that inherit from `VigilisError`.

## Tests

- Every change needs tests. Bug fixes need a test that fails without the fix.
- Test files live in `tests/` and are named `test_<module>.py`. Test functions start with
  `test_`.
- Use the in-memory store and the Argon2 hasher in tests rather than real databases.

## Security-sensitive changes

Vigilis handles credentials, so changes to authentication need extra care:

- Never log, print, or include passwords or hashes in error messages.
- A wrong password and an unknown username must keep raising the same error and taking
  about the same time.
- Never implement cryptography directly. Use established libraries such as argon2-cffi.

## Pull requests

- Describe what the change does and why.
- Make sure all checks pass.
- Keep pull requests focused. Several small pull requests are easier to review than one
  large one.

## License

By contributing, you agree that your contributions will be licensed under the
[Apache License 2.0](../LICENSE)
