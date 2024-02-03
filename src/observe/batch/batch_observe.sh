#!/bin/bash


#run the code saving data for sleepy_time seconds, max_iter times
max_iter=$1
sleepy_time=$2
tag=$3

cd "$GRSOPARENTPATH"

#create the temporary data folder if it does not exist
bash src/shell_utils/create_dir.sh "temp_data_${tag}"
#build the data path if it does not already exist
date_dir=$(date +"%Y/%m/%d")
data_dir="data/$date_dir"
bash src/shell_utils/create_dir.sh $data_dir


for (( i=1; i<=max_iter; i=i+1 ))
do
  # Inform the user of which iteration we are on
  echo "Running iteration $i"
  
  # Start the Python script as a background process, then kill it after sleepy_time seconds
  python3 src/gr/BatchObserve.py $tag &

  #capture the processing id of the script
  pid=$!

  #sleep for the determined amount of seconds
  sleep ${sleepy_time}s

  #kill the observation
  kill $pid

  temp_path="${GRSOPARENTPATH}/temp_data_${tag}"

  data_path="$GRSOPARENTPATH/$data_dir"

  # Move all files from the source to the destination directory
  mv "$temp_path"/* "$data_path"/

  #run the postprocessing as a background script if we have another observational cycle to run
  if (( $i < $max_iter )); then 
    python3 src/observe/batch/proc_batch.py $tag &
  else
  #otherwise, just run as a foreground process so that the script can end gracefully
    python3 src/observe/batch/proc_batch.py $tag
  fi

  #give the script time to stop, so the SDR isnt busy when the new script starts
  # If you give it too much time, there will be deadtime at the start of the spectrograms!
  sleep 0.5s

done

rm -r $temp_path



