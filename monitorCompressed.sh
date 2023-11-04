#!/bin/bash

## ADD SOME ERROR HANDLING!

echo "How many iterations [integer]?"
read max_iter
echo "How long to sleep for [seconds]?"
read sleepy_time

for (( i=1; i<=max_iter; i=i+1 ))
do
  # Inform the user of which iteration we are on
  echo "Running iteration $i"

  # Start the Python script as a background process
  python3 observeCollect.py &
  
  # Capture the Process ID (PID) of the background process
  pid=$!

  # Sleep for 5 seconds before killing the script
  sleep ${sleepy_time}s

  #kill the script
  kill $pid

  #give the script time to stop, so the SDR isnt busy when the new script starts
  sleep 1s
  
  # compute the average spectrogram, save it, then delete all the bulky files
  (cd scripts && python3 CompressedMonitoring.py)
  
done
