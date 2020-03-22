#! /bin/bash

tars_port=5000

echo "Starting ngrok in port ${tars_port}"
ngrok http $tars_port > /dev/null & 
sleep 2 

webhook_url="$(curl -s http://localhost:4040/api/tunnels | jq -r .tunnels[0].public_url)/slack/events"
echo "tars is live at ${webhook_url}"
echo ""
echo ""

docker-compose up
