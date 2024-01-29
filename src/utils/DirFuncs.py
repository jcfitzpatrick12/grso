import os

def list_all_files(parent_dir):
        all_files = []
        #walk through all the subdirectories in data
        for root, dirs, files in os.walk(parent_dir):
            for file in files:
                #full_path = os.path.join(root, file)
                all_files.append(file)  # Store the full path to the file
        return all_files