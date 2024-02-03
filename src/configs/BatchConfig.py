from src.configs import GLOBAL_CONFIG
import pickle

class BatchConfig:
    def __init__(self, tag):
        self.tag = tag
        self.name = f"BatchConfig_{tag}"

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
    

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    
    def set_IF_gain(self, IF_gain):
        self.IF_gain = IF_gain

    
    def set_RF_gain(self, RF_gain):
        self.RF_gain = RF_gain
        
    
    def set_average_over_int(self, average_over_int):
        self.average_over_int = average_over_int

    
    def get_center_freq(self):
        return self.center_freq
    

    def get_samp_rate(self):
        return self.samp_rate

    
    def get_IF_gain(self):
        return self.IF_gain

    
    def get_RF_gain(self):
        return self.RF_gain

    
    def get_spectrogram_kwargs(self):
        return self.spectrogram_kwargs


    def get_average_over_int(self):
        return self.average_over_int


    def save_self(self):
        # Correct the file path string concatenation and open the file in binary write mode
        file_path = f"{GLOBAL_CONFIG.path_to_config_data}/{self.name}.bcfg"  # Ensure GLOBAL_CONFIG.path_to_config_data is defined
        print(f"Saving batch_config for tag {self.tag} to {file_path}.")
        with open(file_path, 'wb') as file:  # Open the file in binary write mode
            pickle.dump(self, file)  



def load_config(tag):
    name = f"BatchConfig_{tag}"
    file_path = f"{GLOBAL_CONFIG.path_to_config_data}/{name}.bcfg"
    
    try:
        with open(file_path, 'rb') as file:  
            instance = pickle.load(file)  
    except Exception as e:
                raise SystemError(f"Error loading config for tag {tag}. Received: {e}")
            
    return instance