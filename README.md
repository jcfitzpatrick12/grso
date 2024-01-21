# grso: GNU Radio for Solar Observations

## Introduction
Software back-end for solar radio observations using ```gnuradio```. Interfacing with SDRPlay RSP1A through [gr-sdrplay3](https://github.com/fventuri/gr-sdrplay3.git). Automated scripts for the continous collection, storing and post-processing radio spectrograms. Designed to work with [```grso-docker```](https://github.com/jcfitzpatrick12/grso-docker.git). 

## Supported Operating Systems

This project is tested to be compatible with the following operating systems:

- Ubuntu 22.04.3

It may also work on other Linux distributions and other Ubuntu versions. However, full compatibility is not guaranteed for operating systems other than the ones listed above.

## Installation
- Please ensure that you have installed [```grso-docker```](https://github.com/jcfitzpatrick12/grso-docker.git). Follow the instructions on this repository

## Usage
This section will be subject to modification in the future. The below commands assume the user has correctly installed [```grso-docker```](https://github.com/jcfitzpatrick12/grso-docker.git). All commands assume you are inside the container, and have cd'd into the ```grso``` directory.

- Running  ```service cron start``` will enable daily observations. 
- Running ```bash src/fMonitor/monitor.sh N M``` will collect ```N``` discrete radio spectrograms, where each data segment is ```M``` seconds long. The spectrogram is saved as a ```fits``` file in the appropriate directory in data according to the time of collection. 
- To visualise the data over some time segment, run ```python3 src/fLook/look_between.py [START_TIME] [END_TIME] power dBb``` where ```[START_TIME]``` and ```[END_TIME]``` are formatted like ```%Y-%m-%dT%H:%M:%S```, and the subsequent arguments indicate which plots to stack in the figure. ```power``` will plot normalised power over the time interval requested, and ```dBb``` will plot the corresponding spectrogram in units of dB above the background.
- Any parameter configurations are made within the module ```src/fConfig/CONFIG.py```

## Contributing
Contributions to `grso-docker` are welcome. If you have suggestions or improvements, please open an issue or submit a pull request on the GitHub repository.

## Improvements to Come
- Support for Raspberry Pi.
- Front-end.
- Custom gnuradio sink block for continous streaming of raw IQ data into spectrograms (current method employs a batch-process approach using the gnuradio block "file meta sink").

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE).

