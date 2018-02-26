#! /bin/bash

SCRIPT=$0
OPTION=$1

main(){

  case "$OPTION" in
    (stop)
      stop
      exit 1
      ;;
    (start)
      start
      exit 0
      ;;
    (status)
      status
      exit 0
      ;;
    (*)
      echo "Usage: $SCRIPT {stop|start}"
      exit 2
      ;;
  esac

}

stop(){
  exec kill -9 `ps aux | grep gunicorn | grep lineage | awk '{ print $2 }'`
}

start(){
  exec gunicorn --workers 3 --bind unix:/home/ec2-user/data-lineage/lineage.sock wsgi --daemon
}

status(){
  exec ps aux | grep gunicorn | grep lineage
}


main
