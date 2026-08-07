#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-2-Clause

set -euo pipefail

release_tag=${1:?usage: pages-release-eligibility.sh <release-tag>}
stable_tag_pattern='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'

if ! git show-ref --verify --quiet "refs/tags/$release_tag"; then
  echo "release tag does not exist: $release_tag" >&2
  exit 1
fi

if [[ $release_tag =~ $stable_tag_pattern ]]; then
  major=${BASH_REMATCH[1]}
  minor=${BASH_REMATCH[2]}
  if (( major > 0 || minor >= 2 )); then
    echo "eligible=true"
    echo "$release_tag is eligible for Pages" >&2
    exit 0
  fi
fi

echo "eligible=false"
echo "$release_tag does not update Pages" >&2
