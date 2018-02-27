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
    sudo neo4j stop
    check_stop
    process=0

    if [[ -d "/var/lib/neo4j/data/databases/graph.db" ]]; then
      sudo cp -R /var/lib/neo4j/data/databases/graph.db \
        /var/lib/neo4j/data/databases/graph.db.bck \
        && sudo rm -rvf /var/lib/neo4j/data/databases/graph.db
      process=$?
    fi

    if [[ ${process} -eq 0 ]]; then
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
    fi
    sudo neo4j start
    wait_for_neo4j
  fi
}

function check_stop {
  echo "STOP"
  sudo kill -9 `ps aux | grep neo4j | awk '{print $2}'`
}

# wait for neo4j
function wait_for_neo4j {
  while ! nc -z localhost 7474; do
    echo "Neo4j is unavailable - sleeping"
    sudo neo4j status
    sleep 1
  done
}

main
