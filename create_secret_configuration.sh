#!/bin/bash

sed -i -e "s/\"NEO4J_PASSWORD\",.*)))/\"NEO4J_PASSWORD\", \"$NEO4J_PASSWORD\")))/g" ./api/settings/db.py
