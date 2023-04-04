#!/bin/bash
<<<<<<< HEAD
#python3 server.py
for i in {1..10}
=======
# python3 test.py &
# pid=$!

# echo "Server process started with PID: $pid"
# sleep 1
for i in {1..2}
>>>>>>> 51c78bfad00ae84830bbc5c34bad8a85272e0fc5
do
    # echo "Client $i started with PID: $pid"
    # python3 client.py > outcome.txt &
    python3 client.py
done

# kill $pid
# echo "Background process terminated"