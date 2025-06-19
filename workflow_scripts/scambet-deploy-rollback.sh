#!/bin/bash

set -euo pipefail

: "${INSTANCE:?Missing INSTANCE}"
: "${VERSION:?Missing VERSION}"
: "${SERVICE:?Missing SERVICE}"

echo "Instance: $INSTANCE"
echo "Version: $VERSION"
echo "Service: $SERVICE"

sudo docker pull ghcr.io/alexprsk/$INSTANCE:$VERSION
sudo docker compose stop $SERVICE || true
sudo docker compose rm $SERVICE || true
sed -i "s|image: ghcr.io/alexprsk/$INSTANCE:.*|image: ghcr.io/alexprsk/$INSTANCE:$VERSION|" docker-compose.yml
sudo docker compose up -d $SERVICE
docker image prune --force