#!/bin/bash

cp -R /code /working_code
chmod -R 777 /working_code
cd /working_code
rm -rf /working_code/venv/
virtualenv -p python3.6 /working_code/venv
python3.6 setup.py sdist --formats=gztar
FILENAME=`python3.6 setup.py --fullname`
FILENAME=${FILENAME}.tar.gz

echo "Starting deploy"

mkdir -p /truedat/td_dl
mkdir -p /truedat/td_dl/scripts
mkdir -p /truedat/td_dl/media/uploads
rm -rf /truedat/td_dl/venv/
virtualenv -p python3.6 /truedat/td_dl/venv
/truedat/td_dl/venv/bin/pip install /working_code/dist/${FILENAME}

cp /working_code/wsgi.py /truedat/td_dl/
cp /working_code/scripts/launchApp.sh /truedat/td_dl/scripts
cp /working_code/scripts/launch_neo4j.sh /truedat/td_dl/scripts
chmod 755 /truedat/td_dl/scripts/launchApp.sh

REGEX="(PROJECT_PATH=)(.*)"
SUST="\1/truedat/td-dl"
sed -i -r "s@${REGEX}@${SUST}@g" /truedat/td_dl/scripts/launchApp.sh

cd /truedat/td_dl
tar cfz td_dl.tar.gz ./
cp td_dl.tar.gz /code/dist/

echo "Finished deployment"
