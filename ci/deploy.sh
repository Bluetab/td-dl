#! /bin/bash

useradd -m fabric
echo "fabric:password" | chpasswd
chsh -s /bin/bash fabric

cp -R /code /working_code

wget http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
rpm -ivh epel-release-6-8.noarch.rpm
yum install git -y
yum install openssh-server openssh-clients -y
cat /etc/ssh/sshd_config | sed "s/PasswordAuthentication no/PasswordAuthentication yes/g" > /etc/ssh/sshd_config
chkconfig sshd on
service sshd start

chmod -R 777 /working_code
chgrp -R fabric /working_code

echo "
export NEO4J_PASSWORD=$NEO4J_PASSWORD
export PRODUCTION_HOST=$PRODUCTION_HOST
export PRODUCTION_USER=$PRODUCTION_USER
export GUARDIAN_SECRET_KEY=$GUARDIAN_SECRET_KEY
export PRODUCTION_PEM=\"$PRODUCTION_PEM\"" >> /working_code/env_vars.sh

chmod +x /working_code/env_vars.sh

su fabric -c '/working_code/ci/deploy_as_fabric.sh'
