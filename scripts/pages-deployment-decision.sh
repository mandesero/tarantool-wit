#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-2-Clause

set -euo pipefail

current_tag=${1:-}
candidate_tag=${2:?usage: pages-deployment-decision.sh <current-tag-or-empty> <candidate-tag>}
stable_tag_pattern='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'

if ! git show-ref --verify --quiet "refs/tags/$candidate_tag"; then
  echo "candidate tag does not exist: $candidate_tag" >&2
  exit 1
fi

if [[ ! $candidate_tag =~ $stable_tag_pattern ]]; then
  echo "deploy=false"
  echo "current-tag=$current_tag"
  echo "skipping non-stable Pages release $candidate_tag" >&2
  exit 0
fi
candidate_major=${BASH_REMATCH[1]}
candidate_minor=${BASH_REMATCH[2]}
candidate_patch=${BASH_REMATCH[3]}

if (( candidate_major == 0 && candidate_minor < 2 )); then
  echo "deploy=false"
  echo "current-tag=$current_tag"
  echo "skipping Pages release before v0.2.0: $candidate_tag" >&2
  exit 0
fi

if [[ -z $current_tag ]]; then
  echo "deploy=true"
  echo "current-tag="
  echo "no existing Pages release; deploying $candidate_tag" >&2
  exit 0
fi

if ! git show-ref --verify --quiet "refs/tags/$current_tag"; then
  echo "published Pages tag is not present in the repository: $current_tag" >&2
  exit 1
fi

if [[ ! $current_tag =~ $stable_tag_pattern ]]; then
  echo "published Pages marker is not a stable release tag: $current_tag" >&2
  exit 1
fi
current_major=${BASH_REMATCH[1]}
current_minor=${BASH_REMATCH[2]}
current_patch=${BASH_REMATCH[3]}

if [[ $current_tag == "$candidate_tag" ]]; then
  echo "deploy=true"
  echo "current-tag=$current_tag"
  echo "redeploying current Pages release $candidate_tag" >&2
elif (( candidate_major > current_major ||
  (candidate_major == current_major && candidate_minor > current_minor) ||
  (candidate_major == current_major && candidate_minor == current_minor &&
    candidate_patch > current_patch) )); then
  echo "deploy=true"
  echo "current-tag=$current_tag"
  echo "Pages release advances from $current_tag to $candidate_tag" >&2
else
  echo "deploy=false"
  echo "current-tag=$current_tag"
  echo "skipping $candidate_tag because Pages already serves $current_tag" >&2
fi
