#!/bin/bash

INSTANCE=$INSTANCE
VERSION=$VERSION
SERVICE=$SERVICE

sudo docker pull ghcr.io/alexprsk/$INSTANCE:$VERSION
sudo docker compose stop $SERVICE || true
sudo docker compose rm $SERVICE || true
sed -i "s|image: ghcr.io/alexprsk/$SERVICE:.*|image: ghcr.io/alexprsk/$SERVICE:$VERSION|" docker-compose.yml
sudo docker compose up -d $SERVICE
docker image prune --force