#!/usr/bin/env bash

docker build -t bluetab-truedat/td-dl:latest .
docker rmi --force $(docker images -f "dangling=true" -q)
