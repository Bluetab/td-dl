#!/bin/bash

rm -f ~/.ssh/lineage.pem
echo "$PRODUCTION_PEM" | sed 's/\r//g' | sed 's/^ //g' > ~/.ssh/lineage.pem
chmod 400 ~/.ssh/lineage.pem
touch ~/.ssh/config
chmod 600 ~/.ssh/config
cp -f ~/.ssh/config ~/.ssh/config.bk
echo "Host ${PRODUCTION_HOST}" > ~/.ssh/config
echo "IdentityFile ~/.ssh/lineage.pem" >>  ~/.ssh/config
chmod 400 ~/.ssh/config
