#!/bin/bash


PYTHON_VERSION="${1:-3.6}"
if [[ ${PYTHON_VERSION} != "3.6" && ${PYTHON_VERSION} != "2" ]]; then
  exit 1
fi

if [[ ${PYTHON_VERSION} == "2" ]]; then
 PYTHON_VERSION=""
fi

docker run --rm -v $(pwd):/code:ro -e PYTHON_VERSION=${PYTHON_VERSION} -v $(pwd)/dist:/code/dist -w /code --entrypoint=/code/build_centos/entrypoint.sh nachohidalgo89/centos-python3:20180523160135
