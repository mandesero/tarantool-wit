#!/usr/bin/env bash
set -euo pipefail

site_dir=${1:?usage: build-pages-site.sh <output-dir> <release-tag>}
release_tag=${2:?usage: build-pages-site.sh <output-dir> <release-tag>}

stable_tag_pattern='^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$'
if [[ ! $release_tag =~ $stable_tag_pattern ]]; then
  echo "Pages release tag must use the stable vMAJOR.MINOR.PATCH form: $release_tag" >&2
  exit 1
fi
release_major=${BASH_REMATCH[1]}
release_minor=${BASH_REMATCH[2]}
release_patch=${BASH_REMATCH[3]}

if ! git rev-parse --verify --quiet "$release_tag^{commit}" >/dev/null; then
  echo "release tag does not exist: $release_tag" >&2
  exit 1
fi

release_commit=$(git rev-parse "$release_tag^{commit}")
head_commit=$(git rev-parse HEAD)
if [[ $release_commit != "$head_commit" ]]; then
  echo "release tag $release_tag does not point to HEAD" >&2
  exit 1
fi

if [[ -d $site_dir && -n $(find "$site_dir" -mindepth 1 -print -quit) ]]; then
  echo "output directory must be empty: $site_dir" >&2
  exit 1
fi

mkdir -p "$site_dir"

work_dir=$(mktemp -d)
trap 'rm -rf "$work_dir"' EXIT

release_tags=()
while IFS= read -r tag; do
  if [[ $tag =~ $stable_tag_pattern ]]; then
    tag_major=${BASH_REMATCH[1]}
    tag_minor=${BASH_REMATCH[2]}
    tag_patch=${BASH_REMATCH[3]}
  else
    continue
  fi

  if (( (tag_major > 0 || tag_minor >= 2) &&
    (tag_major < release_major ||
      (tag_major == release_major && tag_minor < release_minor) ||
      (tag_major == release_major && tag_minor == release_minor &&
        tag_patch <= release_patch)) )); then
    release_tags+=("$tag")
  fi
done < <(git tag --list 'v[0-9]*' --sort=v:refname)

if [[ ${#release_tags[@]} -eq 0 ]]; then
  echo "no documentation release tags found (expected v0.2.0 or newer)" >&2
  exit 1
fi

release_version=${release_tag#v}
release_found=false

write_api_page() {
  local version=$1
  local fragment=$2
  local output=$3

  cat > "$output" <<EOF
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Tarantool WIT API $version">
  <title>Tarantool WIT API $version</title>
  <style>
    :root { color-scheme: light dark; font-family: system-ui, sans-serif; }
    body { margin: 0; line-height: 1.55; }
    header { position: sticky; top: 0; z-index: 1; display: flex; gap: 1rem;
      align-items: center; padding: .8rem max(1rem, calc((100% - 70rem) / 2));
      background: Canvas; border-bottom: 1px solid color-mix(in srgb, CanvasText 18%, transparent); }
    header .brand { font-weight: 700; margin-right: auto; }
    main { max-width: 70rem; margin: 0 auto; padding: 1.5rem 1rem 4rem; }
    h2 { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid
      color-mix(in srgb, CanvasText 16%, transparent); }
    code { padding: .08rem .3rem; border-radius: .25rem;
      background: color-mix(in srgb, CanvasText 8%, transparent); }
    a { color: LinkText; }
    li { margin-block: .25rem; }
    @media (max-width: 42rem) { header { flex-wrap: wrap; } }
  </style>
</head>
<body>
<header>
  <a class="brand" href="../">Tarantool WIT</a>
  <span>API $version</span>
  <a href="../latest/">Latest</a>
  <a href="api.md">Markdown</a>
</header>
<main>
EOF
  cat "$fragment" >> "$output"
  cat >> "$output" <<'EOF'
</main>
</body>
</html>
EOF
}

shopt -s nullglob
for tag in "${release_tags[@]}"; do
  version=${tag#v}
  source_dir="$work_dir/$version/source"
  generated_dir="$work_dir/$version/generated"
  version_dir="$site_dir/$version"
  mkdir -p "$source_dir" "$generated_dir" "$version_dir"

  git archive "$tag" -- wit | tar -x -C "$source_dir"
  wit-bindgen markdown --world guest --out-dir "$generated_dir" "$source_dir/wit"

  html_files=("$generated_dir"/*.html)
  markdown_files=("$generated_dir"/*.md)
  if [[ ${#html_files[@]} -ne 1 || ${#markdown_files[@]} -ne 1 ]]; then
    echo "expected one HTML and one Markdown file for $tag" >&2
    exit 1
  fi

  write_api_page "$version" "${html_files[0]}" "$version_dir/index.html"
  cp "${markdown_files[0]}" "$version_dir/api.md"
  printf '%s\n' "$tag" > "$version_dir/release.txt"

  if [[ $tag == "$release_tag" ]]; then
    release_found=true
  fi
done

if [[ $release_found != true ]]; then
  echo "release tag was not included in generated versions: $release_tag" >&2
  exit 1
fi

mkdir -p "$site_dir/latest"
cp -R "$site_dir/$release_version/." "$site_dir/latest/"

cat > "$site_dir/index.html" <<EOF
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Versioned Tarantool WebAssembly Component Model API documentation">
  <title>Tarantool WIT documentation</title>
  <style>
    :root { color-scheme: light dark; font-family: system-ui, sans-serif; }
    body { max-width: 48rem; margin: 0 auto; padding: 3rem 1rem; line-height: 1.55; }
    a { color: LinkText; }
    li { margin-block: .5rem; }
  </style>
</head>
<body>
  <h1>Tarantool WIT documentation</h1>
  <p>WebAssembly Component Model API definitions for Tarantool guest components.</p>
  <p><a href="latest/"><strong>Latest release ($release_version)</strong></a></p>
  <h2>Published versions</h2>
  <ul>
EOF

for ((index=${#release_tags[@]} - 1; index >= 0; index--)); do
  version=${release_tags[index]#v}
  printf '    <li><a href="%s/">%s</a></li>\n' "$version" "$version" >> "$site_dir/index.html"
done

cat >> "$site_dir/index.html" <<'EOF'
  </ul>
  <p><a href="https://github.com/mandesero/tarantool-wit">Source repository</a></p>
</body>
</html>
EOF

: > "$site_dir/.nojekyll"

echo "generated Pages site for ${#release_tags[@]} releases; latest is $release_tag"
