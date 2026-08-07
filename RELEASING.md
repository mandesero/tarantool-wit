# Releasing tarantool-wit

Releases are created from a clean commit on the default branch. A tag is the
source of truth for the WIT package, OCI artifact, signature, release notes, and
stable API documentation.

## Prepare the version

Choose the next version according to the compatibility policy in `README.md`.
Update every `package tarantool:tarantool@<version>` declaration. Preserve the
existing `@since` value on unchanged declarations; use the new release version
only for declarations introduced by this release.

Move the relevant entries from `Unreleased` in `CHANGELOG.md` to
`[<version>] - YYYY-MM-DD`, add a new empty `Unreleased` section, and update the
comparison links at the bottom of the file. Update migration and API
documentation before tagging.

## Validate the release commit

Run the contract checks with the tool versions pinned in
`.github/workflows/ci.yaml`:

```sh
wkg wit build -d wit -o /tmp/tarantool-tarantool.wasm
wasm-tools validate /tmp/tarantool-tarantool.wasm
wit-bindgen markdown --world guest --out-dir /tmp/tarantool-wit-docs wit
wit-bindgen rust --world guest --out-dir /tmp/tarantool-wit-rust wit
scripts/report-contract-changes.sh /tmp/tarantool-wit-contract-changes.md
scripts/check-release-version.sh vX.Y.Z tag
rm -f wkg.lock
```

Review the generated compatibility report and confirm that every intentional
breaking change is documented. Merge the release preparation only after the
pull request validation succeeds.

## Tag and publish

Create an annotated tag on the validated release commit and push only that tag:

```sh
git tag -a vX.Y.Z -m "tarantool-wit X.Y.Z"
git push origin vX.Y.Z
```

The publish workflow reruns contract validation, verifies that the tag matches
the WIT package version, publishes the package to
`ghcr.io/mandesero/tarantool/tarantool:X.Y.Z`, and signs its immutable digest
with cosign. Stable tags `vMAJOR.MINOR.PATCH` also publish versioned HTML and
Markdown API documentation to GitHub Pages and update `latest`. Prerelease tags
publish the OCI package but do not modify Pages.

## Verify and announce

Confirm that the workflow completed its `validate`, `publish`, and, for a stable
release, `pages` jobs. Check that the OCI digest shown by the registry matches
the digest signed by the workflow. Verify the keyless signature against the
release workflow identity, then fetch the package as a final smoke test:

```sh
cosign verify \
  --certificate-identity \
    "https://github.com/mandesero/tarantool-wit/.github/workflows/publish.yaml@refs/tags/vX.Y.Z" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" \
  ghcr.io/mandesero/tarantool/tarantool@sha256:<digest>

wkg oci pull \
  ghcr.io/mandesero/tarantool/tarantool:X.Y.Z \
  -o /tmp/tarantool-tarantool-X.Y.Z.wasm
wasm-tools validate /tmp/tarantool-tarantool-X.Y.Z.wasm
```

Create a GitHub release from the tag. Use the matching changelog section as the
release notes and link the OCI artifact, versioned API documentation, and
migration guide when applicable.

Do not move or reuse a published tag. Fix release automation or documentation
with a new patch release so the tag, OCI digest, signature, and versioned Pages
URL remain immutable.
