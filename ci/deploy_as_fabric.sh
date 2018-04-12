#! /bin/bash

cd /working_code
/working_code/env_vars.sh

echo "distro requirements"

mkdir -p ~/.ssh
ssh-keygen -t rsa -f ~/.ssh/id_rsa -q -N ""
chmod 600 ~/.ssh/id_rsa*
cat ~/.ssh/id_rsa >> ~/.ssh/authorized_keys
chmod og-wx ~/.ssh/authorized_keys
sshpass -p "password" ssh-copy-id -o StrictHostKeyChecking=no fabric@localhost || exit 1

rm -rf /working_code/venv || exit 1
virtualenv -p python3.6 /working_code/venv
source /working_code/venv/bin/activate
pip install -e .

./add_deployment_keys.sh || exit 1

./create_secret_configuration.sh || exit 1

if [ -z "$SSH_AUTH_SOCK"]; then
  eval `ssh-agent -s`
  ssh-add ~/.ssh/lineage.pem
fi

echo "Starting deploy"
fab pack deploy || exit 1

echo "Finished deployment"
