# Changelog

All notable changes to this project are documented in this file. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and releases
use [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-08-07

### Added

- The aggregate `guest` world and independently importable Tarantool interfaces.
- Opaque host-issued handles with explicit `retain` and `release` operations.
- Copied MessagePack values, tuple fields, and structured Tarantool errors.
- API, migration, architecture, validation, and release documentation.
- CI validation, generated bindings, compatibility reports, and versioned API
  documentation for stable releases starting with `0.2.0`.

### Changed

- Canonical interface names are `database`, `log`, and `transaction`.
- IDs, sizes, enum cases, absence, and failure results now follow the public
  value model defined for `0.2.0`.
- Error codes are open `u32` values so consumers can preserve unknown codes.

### Removed

- Native pointers, raw field addresses, and pointer-based MessagePack decoding
  from the component boundary.
- Runtime-specific logging operations and redundant transaction helpers.

[Unreleased]: https://github.com/mandesero/tarantool-wit/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/mandesero/tarantool-wit/compare/v0.1.4...v0.2.0
