# Security policy

## Supported versions

Security fixes are prepared for the current stable minor line. The `0.1.x`
contract exposes native-pointer-shaped values and is not supported.

| Version | Supported |
| --- | --- |
| `0.2.x` | Yes |
| `0.1.x` | No |

## Reporting a vulnerability

Do not open a public issue for an undisclosed vulnerability. Use
[GitHub private vulnerability reporting](https://github.com/mandesero/tarantool-wit/security/advisories/new).
If that form is unavailable, contact the maintainer at `mandesero@gmail.com`.

Include the affected package version or commit, the interfaces involved, the
security impact, reproduction steps, and any suggested mitigation. Relevant
reports include unsafe boundary representations, handle forgery or reuse,
malformed MessagePack handling, accidental capability exposure, and release or
registry integrity failures.

The maintainer will coordinate validation, remediation, a supported-version
release, and public disclosure with the reporter. Keep details private until a
fixed release and advisory are available.
