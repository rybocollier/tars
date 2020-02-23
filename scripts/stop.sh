#! /bin/bash 

NGROK_PID=$(ps -ef | grep ngrok | grep -v grep | awk '{print $2}')

if [ -z "${NGROK_PID}" ]
then
    echo "ngrok is not running, no need to stop ngrok"
else
    echo "ngrok is running, killing pid ${NGROK_PID}"
    kill $NGROK_PID
fi

docker-compose stop
docker-compose down --volumes --remove-orphans --rmi all
