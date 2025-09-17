#!/usr/bin/env bash
set -euo pipefail

# Usage: ./build_push.sh <repo> [tag] [platforms]
# Examples:
#   ./build_push.sh yourname/inference
#   ./build_push.sh ghcr.io/yourorg/inference v1.0.0 "linux/amd64,linux/arm64"

REPO=${1:?Usage: $0 <repo> [tag] [platforms]}
TAG=${2:-latest}
PLATFORMS=${3:-linux/amd64}

IMAGE="${REPO}:${TAG}"

docker buildx inspect >/dev/null 2>&1 || docker buildx create --use

DOCKER_BUILDKIT=1 docker buildx build \
  --platform "${PLATFORMS}" \
  -t "${IMAGE}" \
  --push .
echo "Pushed ${IMAGE}"
