#!/bin/sh
# Makes the SDK from openapi.json, the API's document: scripts/sdk-document.jq writes the document it
# is generated from, openapi-python-client 0.29.1 generates xipfax_sdk from that with
# openapi-python-client.yaml and the package's root module in templates/, ruff formats what it
# writes by pyproject.toml's settings, and this script writes xipfax_sdk/api_version.py from the
# document's info.version. Nothing it writes is edited by hand. xipfax_sdk/xipfax.py and
# xipfax_sdk/py.typed are the package's own, which it leaves as they are. Nothing is fetched: uv
# runs offline, on the environment uv sync --locked made.
set -eu
cd "$(dirname "$0")/.."
export UV_OFFLINE=1

if ! version=$(jq -er '.info.version | select(test("^[0-9]{4}-[0-9]{2}-[0-9]{2}$"))' openapi.json); then
  echo "openapi.json's info.version is not a day, as 2026-11-03 is." >&2
  exit 1
fi

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
jq -f scripts/sdk-document.jq openapi.json > "$work/openapi.json"

# The generator writes the package's root files again and makes api/ and models/ anew, so that a
# module the document no longer makes doesn't stay. A warning fails it, a missing ruff among them.
uv run --no-sync openapi-python-client generate --path "$work/openapi.json" --meta none \
  --output-path xipfax_sdk --overwrite --config openapi-python-client.yaml \
  --custom-template-path templates --fail-on-warning

cat > xipfax_sdk/api_version.py <<EOF
"""The version of XipFax's API this SDK is generated from, written by scripts/generate.sh from
openapi.json's info.version. Every request names it in its Xip-Version header."""

API_VERSION = "$version"
EOF
