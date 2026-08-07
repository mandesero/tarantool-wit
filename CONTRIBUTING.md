# Contributing

Changes to this repository modify the public Component Model contract used by
Tarantool hosts and guest components. Open an issue before making a breaking or
cross-cutting change so its compatibility and ownership semantics can be agreed
before implementation.

## Contract changes

Keep WIT declarations independent of a particular host language or runtime.
Document MessagePack shapes, ownership, normal absence, and failure behavior at
the declaration that exposes them. New public declarations need an appropriate
`@since` annotation. Existing annotations record when a declaration was
introduced and must not be rewritten during a patch release.

Update `docs/api.md` when behavior changes and the relevant migration guide
(currently `docs/migration-0.2.md`) when a consumer must change. Update the
relevant ADR when an architectural decision changes and `CHANGELOG.md` for
every user-visible modification.

## Local validation

CI pins the supported tool versions in `.github/workflows/ci.yaml`. Install
those versions, then run the same contract checks from the repository root:

```sh
wkg wit build -d wit -o /tmp/tarantool-tarantool.wasm
wasm-tools validate /tmp/tarantool-tarantool.wasm
wit-bindgen markdown --world guest --out-dir /tmp/tarantool-wit-docs wit
wit-bindgen rust --world guest --out-dir /tmp/tarantool-wit-rust wit
scripts/report-contract-changes.sh /tmp/tarantool-wit-contract-changes.md
rm -f wkg.lock
```

Inspect the compatibility report rather than treating every difference as a
failure: intentional contract changes still require migration documentation.
Run `shellcheck scripts/*.sh` and `actionlint` when changing automation.

## Submitting changes

Keep each commit focused on one contract or maintenance task. Include tests or
validation evidence in the pull request, call out compatibility effects, and do
not commit generated packages, bindings, documentation output, or `wkg.lock`.

Contributions are accepted under the repository's [BSD-2-Clause license](LICENSE).
The collective copyright holder name `tarantool-wit contributors` refers to
the contributors recorded in the repository's Git history.
