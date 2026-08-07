#!/usr/bin/env bash
set -euo pipefail

release_tag=${1:?usage: check-release-version.sh <release-tag> <ref-type>}
ref_type=${2:?usage: check-release-version.sh <release-tag> <ref-type>}

if [[ $ref_type != tag ]]; then
  echo "release ref must be a tag, got: $ref_type" >&2
  exit 1
fi

case "$release_tag" in
  v*) release_version=${release_tag#v} ;;
  *)
    echo "release ref must be a tag named v<package-version>: $release_tag" >&2
    exit 1
    ;;
esac

package_versions=$(sed -nE \
  's/^[[:space:]]*package[[:space:]]+[^@;]+@([^;]+);[[:space:]]*$/\1/p' \
  wit/*.wit | sort -u)
version_count=$(printf '%s\n' "$package_versions" | awk 'NF { count++ } END { print count + 0 }')

if [[ $version_count -ne 1 ]]; then
  echo "expected one package version across wit/*.wit, found:" >&2
  printf '%s\n' "$package_versions" >&2
  exit 1
fi

if [[ $package_versions != "$release_version" ]]; then
  echo "package version $package_versions does not match release tag $release_tag" >&2
  exit 1
fi

echo "package version $package_versions matches release tag $release_tag"
