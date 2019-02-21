#! /bin/bash
export APPLICATION_ROOT=/working_code

yum -y install nc

# wait for neo4j
function wait_for_neo4j {
  echo "Waiting for Neo4J."
  while ! nc -z ${NEO4J_HOST} 7474; do
    echo -n "."
    sleep 1
  done
  echo
}

cp -R /code /working_code
cd /working_code
rm -rf /working_code/venv || exit 1
virtualenv -p python3.6 /working_code/venv
source /working_code/venv/bin/activate
pip install -e .[dev]

echo "Starting tests"
python setup.py test || exit 1

wait_for_neo4j

echo "Starting behave"
behave || exit 1

echo "Test step finish successfully"
