#!/bin/bash

docker build . -t us-west2-docker.pkg.dev/public-gcr/ai-workbench
docker push -t us-west2-docker.pkg.dev/public-gcr/ai-workbench