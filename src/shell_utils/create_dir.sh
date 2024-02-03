#take in the dir as the first argument
dir=$1

#if the directory $dir does not exist, create it
if [[ ! -d $dir ]]; then
        mkdir -p $dir
        echo "Directory created: $dir"
fi