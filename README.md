# Vigilis

Framework-agnostic authentication and authorization for Python.

> **Status: pre-alpha.** Vigilis is in early development. The API will change
> and it is not ready for production use.

## Goals

- **Framework-agnostic**: works with FastAPI, Django, Flask, or plain Python.
- **Storage-agnostic**: bring your own database or ORM through small protocols.
- **Authentication**: passwords, tokens, and sessions.
- **Authorization**: composable policies and role-based access control.
- **Typed**: fully type-hinted, checked with mypy in strict mode.
- **Minimal core**: no required dependencies; integrations are optional extras.

## Installation

```bash
pip install vigilis
```

## License

Licensed under the [Apache License 2.0](LICENSE).