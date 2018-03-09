#! /bin/bash

set -x

SCRIPT=$0
OPTION=$1
PROJECT_PATH=/home/ec2-user/td_dl

main(){

  case "$OPTION" in
    (stop)
      stop
      exit 0
      ;;
    (start)
      start
      exit 0
      ;;
    (status)
      status
      exit 0
      ;;
    (restart)
      stop
      start
      exit 0
      ;;
    (*)
      echo "Usage: $SCRIPT {stop|start|restart|status}"
      exit 2
      ;;
  esac

}

stop(){
  stringStatus=`status`
  if [[ ! -z ${stringStatus} ]]; then
    exec kill -9 `ps aux | grep gunicorn | grep td_dl | awk '{ print $2 }'`
  fi
}

start(){
  source ${PROJECT_PATH}/venv/bin/activate
  cd $PROJECT_PATH
  gunicorn --bind 127.0.0.1:4003 wsgi d
}

status(){
  exec ps aux | grep gunicorn | grep td_dl
}

main
