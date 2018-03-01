#!/bin/bash

sed -i -e "s/\"NEO4J_PASSWORD\",.*)))/\"NEO4J_PASSWORD\", \"$NEO4J_PASSWORD\")))/g" ./api/settings/db.py
sed -i -e "s/app.config\['SECRET_KEY'\] = .*/app.config\['SECRET_KEY'\] = \"$GUARDIAN_SECRET_KEY\"/g" ./api/app.py
