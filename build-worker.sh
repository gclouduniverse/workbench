#!/bin/bash

docker build . -t us-west2-docker.pkg.dev/public-gcr/ai-workbench/workbench-cli:latest
docker push us-west2-docker.pkg.dev/public-gcr/ai-workbench/workbench-cli:latest