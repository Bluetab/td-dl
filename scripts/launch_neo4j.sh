#! /bin/bash

docker run --rm -d \
--publish=7474:7474 --publish=7687:7687 \
--name=neo4j-lineage \
bluetab/neo4j-lineage:3.3.1

# docker exec -it neo4j-lineage rm /var/lib/neo4j/data/dbms/auth
# docker exec -it neo4j-lineage bin/neo4j-admin set-initial-password bluetab
# docker restart neo4j-lineage
