#!/bin/bash

make package

echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

docker build -t lifeomic/termlink .

npm_package_version="$(cat package.json | jq .version | sed 's/"//g')"
docker tag lifeomic/termlink lifeomic/termlink:$npm_package_version && docker push lifeomic/termlink:$npm_package_version && docker push lifeomic/termlink:latest