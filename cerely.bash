#!/bin/bash
# function: it starts,stops and restrart cerely
# the file log  in the dir /tmp, like /tmp/cerely_worker20170708122334.log  /tmp/cerely_beat20170708122334.log
# run env: need root user
# usage: chmod 700 cerely.bash && ./cerely.bash {start|stop|restart}
# author: Abner.R
# version: 1.0

function stopCerely() {

    ps -ef | grep -i Celery | awk '{print $2}' | xargs kill  >/dev/null 2>&1

    if [ `ps -ef | grep -i Celery | awk '{print $2}' | xargs kill | wc -l` -ne 0 ];then

        ps -ef | grep -i Celery | awk '{print $2}' | xargs kill -9  >/dev/null 2>&1

    fi

    echo "Cerely stop now ......"

}

function startCerely() {

    source /etc/profile && source /usr/local/venv/bin/activate && cd /data/cobra_main
    nohup python -m celery -A cobra_main worker -l info >/tmp/cerely_worker_`date +'%Y%m%d%H%M%S'`.log 2>&1 &

    if [ `ps  -ef | grep -i celery | wc -l` -gt 0 ];then
        echo "Cerely  beat start now ....."
    fi

    nohup python -m celery -A cobra_main beat -l info >/tmp/cerely_beat_`date +'%Y%m%d%H%M%S'`.log 2>&1 &

    if [ `ps  -ef | grep -i celery | wc -l` -gt 1 ];then
        echo "Cerely  worker start now ....."
    fi

}

function usage() {

   echo "usage: $0 {start|stop|restart}"
   exit 1

}

function main() {

   action=$1

   if [ $# -eq 0 ];then

       usage

   fi

   if [ $action == 'stop' ];then

       stopCerely

   elif [ $action == 'start' ];then

       startCerely

   elif [ $action == 'restart' ];then

       stopCerely
       startCerely

   else

       usage
   fi

}

main $1