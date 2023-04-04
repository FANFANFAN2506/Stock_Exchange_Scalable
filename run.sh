#!/bin/bash
# python3 test.py &
# pid=$!

# echo "Server process started with PID: $pid"
# sleep 1
for i in {1..2}
do
    # echo "Client $i started with PID: $pid"
    # python3 client.py > outcome.txt &
    python3 client.py
done

# kill $pid
# echo "Background process terminated"