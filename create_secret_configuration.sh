#!/bin/bash

sed -i -e "s/NEO4J_PASSWORD = .*/NEO4J_PASSWORD = \"$NEO4J_PASSWORD\"/g" ./api/settings/config.py
sed -i -e "s/REDIS_URI = .*/REDIS_URI = \"$REDIS_URI\"/g" ./api/settings/config.py
sed -i -e "s/SECRET_KEY = .*/SECRET_KEY = \"$GUARDIAN_SECRET_KEY\"/g" ./api/settings/config.py
