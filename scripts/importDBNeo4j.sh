#! /bin/bash

LIST_FILES="$1"
PATH_NEO4J="${2}"
DELIMITER=${3:-;}
ARRAY_DELIMITER=${4:-|}

main(){

  rm -f ${PATH_NEO4J}/import/*

  OLDIFS=$IFS
	IFS=';'
	for file in ${LIST_FILES}; do
    cp ${file} ${PATH_NEO4J}/import/
	done
	IFS=$OLDIFS

  if [[ ${DELIMITER} == ${ARRAY_DELIMITER} ]]; then
    echo "Character ${ARRAY_DELIMITER} specified by array delimiter is the same as specified by delimiter"
    exit 1
  fi

  files_nodes=`ls -1 ${PATH_NEO4J}/import/nodes_*`
  files_rels=`ls -1 ${PATH_NEO4J}/import/rels_*`

  if [[ ! -z "${files_nodes:-}" || ! -z "${files_rels:-}" ]]; then

    rm -rvf ${PATH_NEO4J}/data/databases/*.bck
    ${PATH_NEO4J}/bin/neo4j stop
    check_stop
    process=0

    if [[ -d "${PATH_NEO4J}/data/databases/graph.db" ]]; then
      cp -R ${PATH_NEO4J}/data/databases/graph.db \
        ${PATH_NEO4J}/data/databases/graph.db.bck \
        && rm -rvf ${PATH_NEO4J}/data/databases/graph.db
      process=$?
    fi

    if [[ ${process} -eq 0 ]]; then
      command_exec="${PATH_NEO4J}/bin/neo4j-admin import --database graph.db "
      for fileNode in $files_nodes; do
      	command_exec+="--nodes ${fileNode} "
      done
      for fileRels in $files_rels; do
      	command_exec+="--relationships ${fileRels} "
      done
      command_exec+="--multiline-fields true --delimiter \"${DELIMITER}\" --array-delimiter \"${ARRAY_DELIMITER}\" --ignore-missing-nodes"
      echo "${command_exec}" | sh
      importStatus=$?
      if [[ ${importStatus} -ne 0 ]]; then
        rm -rvf ${PATH_NEO4J}/data/databases/graph.db
        cp -R ${PATH_NEO4J}/data/databases/graph.db.bck ${PATH_NEO4J}/data/databases/graph.db
      fi
    fi
    ${PATH_NEO4J}/bin/neo4j start
    wait_for_neo4j
  fi
}

function check_stop {
  echo "STOP"
  list_proccess=`ps aux | grep -i $(whoami) | grep -iv grep | grep neo4j | awk '{print $2}'`
  if [[ -z "${list_proccess:-}" ]]; then
    kill -9 ${list_proccess}
  fi
}

# wait for neo4j
function wait_for_neo4j {
  while ! nc -z localhost 7687 ; do
    echo "Neo4j is unavailable - sleeping"
    ${PATH_NEO4J}/bin/neo4j status
    sleep 1
  done

  while ! nc -z localhost 7474 ; do
    echo "Neo4j is unavailable - sleeping"
    ${PATH_NEO4J}/bin/neo4j status
    sleep 1
  done
}

main
