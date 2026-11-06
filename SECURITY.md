# Security Policy

Vigilis is an authentication and authorization library, so security issues are taken
seriously. Thank you for helping keep Vigilis and its users safe.

## Supported versions

Vigilis is in pre-alpha. Only the latest release receives security fixes.

| Version | Supported |
|---|---|
| Latest release | Yes |
| Older releases | No |

## Reporting a vulnerability

**Please do not report security vulnerabilities through public GitHub issues,
discussions, or pull requests.**

Report them privately through GitHub's
[private vulnerability reporting](https://github.com/alimunfed17/vigilis/security/advisories/new).

Please include as much of the following as you can:

- A description of the vulnerability and its impact.
- The affected version or commit.
- Steps to reproduce, ideally with a minimal code example.
- Any suggested fix or mitigation.

## What to expect

1. You will receive an acknowledgement of your report.
2. The report will be investigated and you will be told whether it is accepted.
3. If accepted, a fix will be prepared privately and released as soon as possible.
4. A security advisory will be published with the release. You will be credited for the
   discovery unless you prefer to remain anonymous.

Please give the maintainers reasonable time to release a fix before disclosing the issue
publicly.

## Scope

Examples of issues that are in scope:

- Authentication bypass, such as logging in without valid credentials.
- Leaks that reveal whether a username exists, through error messages or timing.
- Weaknesses in how passwords are hashed or verified.
- Any way to obtain another user's identity.

Issues in applications built with Vigilis, or in third-party dependencies, should be
reported to those projects. If a dependency issue affects Vigilis directly, please let us
know as well.
