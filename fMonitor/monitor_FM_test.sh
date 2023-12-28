#!/bin/bash


#basically, run the code saving data each minute, for 8 hours
max_iter=$1
sleepy_time=$2

cd "$GRSOPARENTPATH"

for (( i=1; i<=max_iter; i=i+1 ))
do
  # Inform the user of which iteration we are on
  echo "Running iteration $i"

  # Start the Python script as a background process, then kill it after sleepy_time seconds
  python3 fGNU/FM_observing_test.py &

  #capture the processing id of the script
  pid=$!

  #sleep for the determined amount of seconds
  sleep ${sleepy_time}s

  #kill the observation
  kill $pid

  #give the script time to stop, so the SDR isnt busy when the new script starts
  sleep 1s

  #Move all files in temp_data to data
  src_dir="$GRSOPARENTPATH/temp_data"
  dest_dir="$GRSOPARENTPATH/data"

  # Move all files from the source to the destination directory
  mv "$src_dir"/* "$dest_dir"/

  #run the postprocessing as a background script if we have another observational cycle to run
  if (( $i < $max_iter )); then 
    python3 fMonitor/post_proc.py &
  else
  #otherwise, just run as a foreground process so that the script can end gracefully
    python3 fMonitor/post_proc.py
  fi

done




