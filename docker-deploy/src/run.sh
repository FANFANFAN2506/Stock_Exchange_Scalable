#!/bin/bash
# python3 test.py &
# pid=$!

echo "Server process started with PID:"
# sleep 1
python3 server.py > serveroutcome.txt &
#python3 /test/client_test.py
while true; do continue; done

# kill $pid
# echo "Background process terminated"