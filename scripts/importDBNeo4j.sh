#! /bin/bash

LIST_FILES="$1"
DELIMITER=$2
ARRAY_DELIMITER=$3

main(){

  sudo rm /var/lib/neo4j/import/*

  OLDIFS=$IFS
	IFS=';'
	for file in ${LIST_FILES}; do
    sudo cp ${file} /var/lib/neo4j/import/
	done
	IFS=$OLDIFS

  if [[ ${DELIMITER:-;} == ${ARRAY_DELIMITER:-|} ]]; then
    echo "Character ${ARRAY_DELIMITER:-|} specified by array delimiter is the same as specified by delimiter"
    exit 1
  fi

  files_nodes=`ls -1 /var/lib/neo4j/import/nodes_*`
  files_rels=`ls -1 /var/lib/neo4j/import/rels_*`

  if [[ ! -z "${files_nodes:-}" || ! -z "${files_rels:-}" ]]; then

    sudo rm -rvf /var/lib/neo4j/data/databases/*.bck

    sudo cp -R /var/lib/neo4j/data/databases/graph.db /var/lib/neo4j/data/databases/graph.db.bck
    copyStatus=$?

    if [[ ${copyStatus} -eq 0 ]]; then
      sudo neo4j stop
      sudo rm -rvf /var/lib/neo4j/data/databases/graph.db

      command_exec="sudo neo4j-admin import --database graph.db "
      for fileNode in $files_nodes; do
      	command_exec+="--nodes ${fileNode} "
      done
      for fileRels in $files_rels; do
      	command_exec+="--relationships ${fileRels} "
      done
      command_exec+="--multiline-fields true --delimiter \"${DELIMITER:-;}\" --array-delimiter \"${ARRAY_DELIMITER:-|}\" --ignore-missing-nodes"
      echo "${command_exec}" | sh
      importStatus=$?
      if [[ ${importStatus} -ne 0 ]]; then
        sudo rm -rvf /var/lib/neo4j/data/databases/graph.db
        sudo cp -R /var/lib/neo4j/data/databases/graph.db.bck /var/lib/neo4j/data/databases/graph.db
      fi
      sudo neo4j start

      wait_for_neo4j
    fi
  fi
}

# wait for neo4j
function wait_for_neo4j {
  while ! nc -z localhost 7474; do
    echo "Neo4j is unavailable - sleeping"
    sleep 1
  done
}

main
