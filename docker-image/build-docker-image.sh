#!/bin/bash

echo "Gerando imagem docker"

DOCKER_IMAGE=gradify
docker build -t $DOCKER_IMAGE .

echo "Imagem $DOCKER_IMAGE criada!"

# TODO deixar uma forma de fazer build ou push, de acordo com parametro
#docker tag gradify luizroos/gradify:0.1
#docker push luizroos/gradify:0.1
