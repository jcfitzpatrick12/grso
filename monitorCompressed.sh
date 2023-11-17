#!/bin/bash

## ADD SOME ERROR HANDLING!

echo "How many iterations [integer]?"
read max_iter
echo "How long to sleep for [seconds]?"
read sleepy_time

# Define the path to the Python interpreter in your Conda environment
ENV_PYTHON="/home/jimmy/miniconda3/envs/gbo-env/bin/python3"

for (( i=1; i<=max_iter; i=i+1 ))
do
  echo "Running iteration $i"

  # Start the Python script using the Python interpreter from your Conda environment
  $ENV_PYTHON observeCollect.py &
  pid=$!

  # Sleep and then kill the script
  sleep ${sleepy_time}s
  kill $pid
  sleep 1s

  # Run the compression script using the same Python interpreter
  (cd scripts && $ENV_PYTHON CompressedMonitoring.py)
done
