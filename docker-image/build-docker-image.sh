#!/bin/bash

echo "Gerando imagem docker"

DOCKER_IMAGE_NAME=gpe
DOCKER_IMAGE_VERSION=0.1
DOCKER_IMAGE="$DOCKER_IMAGE_NAME:$DOCKER_IMAGE_VERSION"

docker build -t $DOCKER_IMAGE .

echo "Imagem $DOCKER_IMAGE criada!"