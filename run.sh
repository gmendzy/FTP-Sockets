#!/bin/bash
kill $(pgrep -f server_final.py)
rm received.txt
./server_final.py &
server_pid=$!
sleep 3
printf "put test.txt\nls" | ./client_final.py
kill $(pgrep -f server_final.py)