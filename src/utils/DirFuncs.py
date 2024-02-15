import os


def list_all_files(parent_dir):
        all_files = []
        #walk through all the subdirectories in data
        for root, dirs, files in os.walk(parent_dir):
            for file in files:
                #full_path = os.path.join(root, file)
                all_files.append(file)  # Store the full path to the file
        return all_files


def return_temp_file_path(chunk_start_time, tag):
	root_temp_path = os.path.join(os.environ['GRSOPARENTPATH'],f"temp_data_{tag}")

	if not os.path.exists(root_temp_path):
		os.mkdir(root_temp_path)
		
	data_path = os.path.join(root_temp_path,f"{chunk_start_time}_{tag}")
	return data_path

