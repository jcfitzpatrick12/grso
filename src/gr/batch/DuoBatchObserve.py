#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, blocks
from gnuradio import sdrplay3
import pmt

from src.configs import GLOBAL_CONFIG
from src.configs.JsonConfig import load_config
from src.gr.batch.MetaDict import MetaDict
from src.gr.batch import TimeStamper  



from gnuradio import qtgui

class DuoBatchObserve(gr.top_block, Qt.QWidget):

    def __init__(self, tags):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Collecting data.")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "DuoBatchObserve")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################

        config_dict_0 = load_config("batch", tags[0])
        config_dict_1 = load_config("batch", tags[1])

        self.samp_rate_0 = config_dict_0['samp_rate']
        self.samp_rate_1 = config_dict_1['samp_rate']

        if self.samp_rate_0 != self.samp_rate_1:
            raise ValueError(f"Sample rates must be equal. samp_rate_0: {samp_rate_0}, samp_rate_1: {samp_rate_1}")

        self.samp_rate = self.samp_rate_0

        self.IF_gain_0 = config_dict_0 ['IF_gain']
        self.IF_gain_1 = config_dict_1['IF_gain']
    

        self.RF_gain_0 = config_dict_0['RF_gain']
        self.RF_gain_1 = config_dict_1['RF_gain']


        self.center_freq_0 = config_dict_0['center_freq']
        self.center_freq_1 = config_dict_1['center_freq']

        self.chunk_start_time = TimeStamper.return_time_now_as_string()

        ##################################################
        # Blocks
        ##################################################
        self.sdrplay3_rspduo_0 = sdrplay3.rspduo(
            '',
            rspduo_mode="Dual Tuner (independent RX)",
            antenna="Both Tuners",
            stream_args=sdrplay3.stream_args(
                output_type='fc32',
                channels_size=2
            ),
        )
        self.sdrplay3_rspduo_0.set_sample_rate(self.samp_rate)
        self.sdrplay3_rspduo_0.set_center_freq(self.center_freq_0, self.center_freq_1)
        self.sdrplay3_rspduo_0.set_bandwidth(self.samp_rate)
        self.sdrplay3_rspduo_0.set_antenna("Both Tuners")
        self.sdrplay3_rspduo_0.set_gain_modes(False, False)
        self.sdrplay3_rspduo_0.set_gain(self.IF_gain_0, self.IF_gain_1, 'IF')
        self.sdrplay3_rspduo_0.set_gain(self.RF_gain_0, self.RF_gain_1, 'RF')
        self.sdrplay3_rspduo_0.set_freq_corr(0)
        self.sdrplay3_rspduo_0.set_dc_offset_mode(False)
        self.sdrplay3_rspduo_0.set_iq_balance_mode(False)
        self.sdrplay3_rspduo_0.set_agc_setpoint(-30)
        self.sdrplay3_rspduo_0.set_rf_notch_filter(False)
        self.sdrplay3_rspduo_0.set_dab_notch_filter(False)
        self.sdrplay3_rspduo_0.set_am_notch_filter(False)
        self.sdrplay3_rspduo_0.set_biasT(False)
        self.sdrplay3_rspduo_0.set_debug_mode(False)
        self.sdrplay3_rspduo_0.set_sample_sequence_gaps_check(False)
        self.sdrplay3_rspduo_0.set_show_gain_changes(False)


        temp_file_path_0 = TimeStamper.return_temp_file_path(self.chunk_start_time, tags[0])
        temp_file_path_1 = TimeStamper.return_temp_file_path(self.chunk_start_time, tags[1])
        
        md_0 = MetaDict()
        meta_dict_0 = md_0.get_dict(self.samp_rate,self.center_freq_0,self.chunk_start_time)
        self.blocks_file_meta_sink_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, temp_file_path_0, self.samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, meta_dict_0, True)
        self.blocks_file_meta_sink_0.set_unbuffered(False)

        md_1 = MetaDict()
        meta_dict_1 = md_0.get_dict(self.samp_rate,self.center_freq_1,self.chunk_start_time)
        self.blocks_file_meta_sink_1 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, temp_file_path_1, self.samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, meta_dict_1, True)
        self.blocks_file_meta_sink_1.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.sdrplay3_rspduo_0, 0), (self.blocks_file_meta_sink_0, 0))
        self.connect((self.sdrplay3_rspduo_0, 1), (self.blocks_file_meta_sink_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rsp_duo_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()




def main(tags, top_block_cls=DuoBatchObserve, options=None):

    '''
    # Parsing command line arguments
    if len(sys.argv) != 4:
        print("Make sure you're passing in the right number of arguments! We need center_freq, samp_rate and IF_gain.")
        sys.exit(1)

    center_freq = float(sys.argv[1])
    samp_rate = float(sys.argv[2])
    IF_gain = float(sys.argv[3])
   
    '''

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(tags)

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    try:
        tags_int = sys.argv[1:]
    except:
        raise ValueError("Please specify the tag by passing in through the command line.")

    tags = []
    for tag in tags_int:
        if tag not in GLOBAL_CONFIG.defined_tags:
            raise ValueError(f"Please specify a valid tag. Received {tag}, need one of {GLOBAL_CONFIG.defined_tags}")
        tags.append(str(tag))
    
    main(tags)
