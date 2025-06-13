#!/bin/bash

INSTANCE=$INSTANCE
VERSION=$VERSION
SERVICE=$SERVICE

echo "Instance is set to:$INSTANCE"
echo "version is set to:$VERSION"
echo "service is set to:$SERVICE"

sudo docker pull ghcr.io/alexprsk/$INSTANCE:$VERSION
sudo docker compose stop $SERVICE || true
sudo docker compose rm $SERVICE || true
sed -i "s|image: ghcr.io/alexprsk/$INSTANCE:.*|image: ghcr.io/alexprsk/$INSTANCE:$VERSION|" docker-compose.yml
sudo docker compose up -d $SERVICE
docker image prune --force