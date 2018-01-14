#!/bin/bash

echo "starting virtual env for voiceminder"
source voiceminder.env

echo "Starting voiceminder server in background"
python3 src/run.py &
SERVER_PID=$!

sleep 5

echo "Launching two echo client users..."

python3 echoapp_client.py --host ws://localhost:5000/websocket/ --test -n kevin &
FIRST_USER_PID=$!
sleep 2

python3 echoapp_client.py --host ws://localhost:5000/websocket/ --test -n tyler &
SECOND_USER_PID=$!
sleep 2

read -p "Press any key to terminate shell script... \n" -n1 -s


echo "terminating clients"
kill $SECOND_USER_PID
kill $FIRST_USER_PID
echo "terminating server"
kill $SERVER_PID