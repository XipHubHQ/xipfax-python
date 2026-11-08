#!/bin/sh
# The repository's gate, run before every pull request: the SDK as openapi.json generates it,
# formatted and linted by ruff, typechecked by mypy with its specs and examples, and built. The
# specs run once before each release, by uv run --no-sync pytest, not here. Nothing is fetched: uv
# runs offline, on the environment uv sync --locked made, and builds with its own backend.
set -eu
cd "$(dirname "$0")/.."
export UV_OFFLINE=1

sh scripts/generate.sh

# The package as the generate left it, against the commit: a module that differs, is new or is gone
# fails the gate.
changed=$(git status --porcelain --untracked-files=all -- xipfax_sdk)
if [ -n "$changed" ]; then
  echo "xipfax_sdk differs from what openapi.json generates: run scripts/generate.sh and commit it." >&2
  echo "$changed" >&2
  exit 1
fi

uv run --no-sync ruff format --check .
uv run --no-sync ruff check .
uv run --no-sync mypy

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
uv build --out-dir "$work"
echo "Gates: GREEN"
