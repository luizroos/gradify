#!/bin/bash

COMMAND=$1
IMAGE_NAME=gradify
TAG_NAME=luizroos/gradify
VERSION=0.3.0

if [[ "$COMMAND" == "clean-local" ]]; then  
  # Filtra as imagens 'gradify' e as remove
  image_ids=$(docker images | grep "gradify" | awk '{print $3}' | sort -u)
  if [ -n "$image_ids" ]; then
    echo "Imagens gradify encontradas: $image_ids"
    echo $image_ids | xargs docker rmi -f
  fi

  # Filtra as imagens dangling e as remove
  dangling_images=$(docker images -f dangling=true -q)
  if [ -n "$dangling_images" ]; then
    echo "Imagens dangling encontradas: $dangling_images"
    echo $dangling_images | xargs docker rmi -f
  fi
  exit 0
fi

echo "Gerando imagem docker, versão $VERSION..."
docker build \
  --build-arg BUILD_DATE="$(date '+%Y-%m-%d %H:%M:%S')" \
  --build-arg GRADIFY_VERSION=$VERSION \
  --label version=$VERSION \
  -t $IMAGE_NAME .
docker tag $IMAGE_NAME $TAG_NAME
echo "Imagem $IMAGE_NAME criada!"

if [[ "$COMMAND" == "push" ]]; then  
  echo "Fazendo push da imagem..."
  if [[ -z "$VERSION" ]]; then
    echo "Erro: A versão não foi especificada."
    exit 1
  fi  
  docker tag gradify $TAG_NAME:$VERSION
  docker push $TAG_NAME:$VERSION
  docker push $TAG_NAME:latest
  docker rmi $TAG_NAME:$VERSION
fi