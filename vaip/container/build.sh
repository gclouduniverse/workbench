#!/bin/bash

TAG="us.gcr.io/ml-lab-152505/model-poc"

docker build --no-cache -f Dockerfile -t "${TAG}" .
docker push "${TAG}"