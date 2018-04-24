#! /bin/bash

yum -y install nc

# wait for neo4j
function wait_for_neo4j {
  while ! nc -z localhost 7474; do
    echo "Neo4j is unavailable - sleeping"
    sleep 1
  done
}

echo "Starting neo4j service"
/neo4j/bin/neo4j start

wait_for_neo4j

rm /neo4j/data/dbms/auth

/neo4j/bin/neo4j-admin set-initial-password bluetab

/neo4j/bin/neo4j restart

wait_for_neo4j

cp -R /code /working_code
cd /working_code
mkdir -p /working_code/api/media/uploads
sed -i -e "s/sudo\s//g" ./scripts/*

rm -rf /working_code/venv || exit 1
virtualenv -p python3.6 /working_code/venv
source /working_code/venv/bin/activate
pip install -e .[dev]

echo "Starting tests"
python setup.py test || exit 1

export APP_ENV=Testing
echo "Starting behave"
behave || exit 1

echo "Test step finish successfully"
