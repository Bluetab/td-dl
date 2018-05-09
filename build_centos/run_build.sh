#!/bin/bash

docker run --rm -v $(pwd):/code:ro -v $(pwd)/dist:/code/dist -w /code --entrypoint=/code/build_centos/entrypoint.sh nachohidalgo89/centos-python3:20180509154830
