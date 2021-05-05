#!/bin/bash

DOCKERFILE=$1
OUTPUTIMAGE=$2
INPUTIMAGE=$3

if [ -n "$3" ]; then
    docker pull $INPUTIMAGE
fi

docker build -f $DOCKERFILE -t $OUTPUTIMAGE .
docker push ghcr.io/fred-mabs/$OUTPUTIMAGE
