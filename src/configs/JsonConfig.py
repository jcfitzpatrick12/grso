from src.configs import GLOBAL_CONFIG
import json

def save_config(config_type, tag, config_dict):
    #### ---- ####
    #    tbd     #
    #### ---- ####

    # for use in some GUI page
    pass


def load_config(config_type, tag):
    """
    Load a JSON file and return it as a dictionary.

    :param json_file_path: Path to the JSON file to be loaded.
    :return: A dictionary representation of the JSON data.
    """
    name = f"{config_type}_config_{tag}"
    file_path = f"{GLOBAL_CONFIG.path_to_config_data}/{name}.json"
    try:
        with open(file_path, 'r') as file:
            config_dict = json.load(file)
            return config_dict
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
        return None
