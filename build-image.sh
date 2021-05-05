#!/bin/bash

USERNAME=$1
CR_PAT=$2
DOCKERFILE=$3
OUTPUTIMAGE=$4
INPUTIMAGE=$5

echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin

if [ -n "$INPUTIMAGE" ]; then
    docker pull ghcr.io/fred-mabs/$INPUTIMAGE
fi

docker build -f $DOCKERFILE -t $OUTPUTIMAGE .
docker tag $OUTPUTIMAGE ghcr.io/fred-mabs/$OUTPUTIMAGE
docker push ghcr.io/fred-mabs/$OUTPUTIMAGE
