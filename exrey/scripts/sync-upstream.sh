#!/usr/bin/env bash
set -euo pipefail

REPO="gorhill/uBlock"

EXREY_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

usage() {
  cat <<'EOF'
Usage:
  sync-upstream.sh [TAG]

Downloads a tagged uBlock Origin release from GitHub and refreshes the vendored
sources under exrey/.

Arguments:
  TAG   Optional. Example: 1.68.0

Environment:
  UBO_TAG   Same as TAG argument
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

TAG="${1:-${UBO_TAG:-}}"
if [[ -z "$TAG" ]]; then
  if command -v curl >/dev/null 2>&1; then
    if command -v python3 >/dev/null 2>&1; then
      TAG="$(
        curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
          | python3 -c 'import json,sys; print(json.load(sys.stdin)["tag_name"])'
      )"
    else
      set +o pipefail
      TAG="$(
        curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" \
          | sed -n 's/\s*"tag_name":\s*"\([^"]\+\)".*/\1/p' \
          | head -n 1
      )"
      set -o pipefail
    fi
  fi
fi

if [[ -z "$TAG" ]]; then
  echo "Unable to determine a uBlock Origin tag to download." >&2
  echo "Specify one as an argument: sync-upstream.sh 1.68.0" >&2
  exit 1
fi

ARCHIVE_URL="https://github.com/${REPO}/archive/refs/tags/${TAG}.tar.gz"

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

ARCHIVE_PATH="$TMP_DIR/ubo.tar.gz"

echo "Fetching ${REPO}@${TAG}..." >&2
curl -fsSL -o "$ARCHIVE_PATH" "$ARCHIVE_URL"

ROOT_DIR_NAME="uBlock-${TAG}"
tar -xzf "$ARCHIVE_PATH" -C "$TMP_DIR"
SRC_DIR="$TMP_DIR/$ROOT_DIR_NAME"

# Keep this repo lightweight and Chromium-focused.
rm -rf \
  "$SRC_DIR/.github" \
  "$SRC_DIR/dist" \
  "$SRC_DIR/docs" \
  "$SRC_DIR/publish-extension"

if [[ -d "$SRC_DIR/platform" ]]; then
  find "$SRC_DIR/platform" -mindepth 1 -maxdepth 1 -type d \
    ! -name 'chromium' \
    ! -name 'common' \
    -exec rm -rf {} +
fi

mkdir -p "$EXREY_DIR"

# Refresh everything under exrey/ except our own scripts.
find "$EXREY_DIR" -mindepth 1 -maxdepth 1 \
  ! -name 'scripts' \
  -exec rm -rf {} +

(
  shopt -s dotglob
  cp -a "$SRC_DIR"/* "$EXREY_DIR/"
)

echo "exrey/ refreshed from ${REPO}@${TAG}" >&2
