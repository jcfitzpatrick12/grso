from src.spectrogram.callisto.RadioSpectrogram import RadioSpectrogram as CallistoRadioSpectrogram
from src.spectrogram.standard.RadioSpectrogram import RadioSpectrogram

tag_to_radio_spectrogram_dict = {
    "00": RadioSpectrogram,
    "02": RadioSpectrogram,
    "03": RadioSpectrogram,
    "01": CallistoRadioSpectrogram,
}

