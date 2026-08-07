#!/usr/bin/env bash
# SPDX-License-Identifier: BSD-2-Clause

set -euo pipefail

report_path=${1:-contract-changes.md}
base_tag=${CONTRACT_BASE_TAG:-}
exclude_tag=${CONTRACT_EXCLUDE_TAG:-}

if [[ -z $base_tag ]]; then
  while IFS= read -r candidate; do
    if [[ $candidate != "$exclude_tag" ]]; then
      base_tag=$candidate
      break
    fi
  done < <(git tag --list 'v[0-9]*' --sort=-v:refname)
fi

mkdir -p "$(dirname "$report_path")"

if [[ -z $base_tag ]]; then
  cat > "$report_path" <<'EOF'
## WIT contract changes

No published version tag was found; there is no baseline to compare.
EOF
  exit 0
fi

work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT

git archive "$base_tag" -- wit | tar -x -C "$work_dir"
wasm-tools component wit --json "$work_dir/wit" | jq -S . > "$work_dir/base.json"
wasm-tools component wit --json wit | jq -S . > "$work_dir/current.json"

diff_status=0
diff -u \
  --label "$base_tag" \
  --label working-tree \
  "$work_dir/base.json" \
  "$work_dir/current.json" > "$work_dir/contract.diff" || diff_status=$?

if [[ $diff_status -gt 1 ]]; then
  echo "failed to compare WIT contracts" >&2
  exit "$diff_status"
fi

if [[ $diff_status -eq 0 ]]; then
  summary="No contract changes detected."
else
  summary="Contract changes detected; review the semantic JSON diff below."
fi

{
  echo "## WIT contract changes"
  echo
  echo "Baseline: \`$base_tag\`"
  echo
  echo "$summary"
  echo
  echo '```diff'
  cat "$work_dir/contract.diff"
  echo '```'
} > "$report_path"
