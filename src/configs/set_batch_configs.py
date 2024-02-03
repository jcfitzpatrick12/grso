from src.configs.BatchConfig import BatchConfig
import scipy.signal as signal

def main():

    ###########################################

    batch_config = BatchConfig("00")
    batch_config.set_center_freq(50.95e6)
    batch_config.set_samp_rate(1e6)
    batch_config.set_IF_gain(-25)
    batch_config.set_RF_gain(0)
    batch_config.set_average_over_int(100)
    batch_config.save_self()

    ###########################################

    batch_config = BatchConfig("02")
    batch_config.set_center_freq(408e6)
    batch_config.set_samp_rate(1e6)
    batch_config.set_IF_gain(-25)
    batch_config.set_RF_gain(0)
    batch_config.set_average_over_int(100)
    batch_config.save_self()

    ###########################################

    batch_config = BatchConfig("03")
    batch_config.set_center_freq(95.8e6)
    batch_config.set_samp_rate(300e3)
    batch_config.set_IF_gain(-50)
    batch_config.set_RF_gain(0)
    batch_config.set_average_over_int(1)
    batch_config.save_self()

    ###########################################

if __name__ == "__main__":
    main()