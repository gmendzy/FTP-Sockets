#!/bin/bash

# Setup
kill $(pgrep -f server_final.py)
rm uploaded.txt
rm downloaded.txt

# Run server in background
./server_final.py &

# Allow time for server to create listening server
sleep 3

# Run basic FTP client operations
printf "put test.txt\nls\nget test.txt" | ./client_final.py

# Teardown
kill $(pgrep -f server_final.py)