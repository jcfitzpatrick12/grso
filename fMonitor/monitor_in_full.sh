#!/bin/bash

## ADD SOME ERROR HANDLING!

echo "How many iterations [integer]?"
read max_iter
echo "How long to sleep for [seconds]?"
read sleepy_time


cd "$GBOPARENTPATH"

for (( i=1; i<=max_iter; i=i+1 ))
do
  # Inform the user of which iteration we are on
  echo "Running iteration $i"

  # Start the Python script as a background process, then kill it after sleepy_time seconds
  python3 fGNU/observeCollect.py &

  #capture the processing id of the script
  pid=$!

  #sleep for the determined amount of seconds
  sleep ${sleepy_time}s

  #kill the observation
  kill $pid

  #give the script time to stop, so the SDR isnt busy when the new script starts
  sleep 1s

  #Move all files in temp_data to data
  src_dir="$GBOPARENTPATH/temp_data"
  dest_dir="$GBOPARENTPATH/data"

  # Move all files from the source to the destination directory
  mv "$src_dir"/* "$dest_dir"/

done




