#!/bin/bash

sed -i -e "s/NEO4J_PASSWORD = .*/NEO4J_PASSWORD = \"$NEO4J_PASSWORD\"/g" ./api/settings/config.py
sed -i -e "s/SECRET_KEY = .*/SECRET_KEY = \"$GUARDIAN_SECRET_KEY\"/g" ./api/settings/config.py
sed -i -e "s/app.config.from_object('api.settings.config.DevelopmentConfig')/app.config.from_object('api.settings.config.ProductionConfig')/g" ./api/app.py
