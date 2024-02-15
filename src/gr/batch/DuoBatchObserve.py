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
from datetime import datetime

from src.utils import Tags, PMTFuncs, DirFuncs
from src.configs import GLOBAL_CONFIG
from src.configs.JsonConfig import load_config 



from gnuradio import qtgui

class DuoBatchObserve(gr.top_block, Qt.QWidget):

    def __init__(self, tag_1, tag_2):
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

        config_dict_1 = load_config("batch", tag_1)
        self.samp_rate_1 = config_dict_1['samp_rate']
        self.IF_gain_1 = config_dict_1['IF_gain']
        self.RF_gain_1 = config_dict_1['RF_gain']
        self.center_freq_1 = config_dict_1['center_freq']

        config_dict_2 = load_config("batch", tag_2)
        self.samp_rate_2 = config_dict_2['samp_rate']
        self.IF_gain_2 = config_dict_2['IF_gain']
        self.RF_gain_2 = config_dict_2['RF_gain']
        self.center_freq_2 = config_dict_2['center_freq']

        if self.samp_rate_1 != self.samp_rate_2:
            raise ValueError(f"Sample rates must be equal. samp_rate_0: {samp_rate_0}, samp_rate_1: {samp_rate_1}")

        self.samp_rate = self.samp_rate_1


        self.chunk_start_time = datetime.now().strftime(GLOBAL_CONFIG.default_time_format)

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
        self.sdrplay3_rspduo_0.set_center_freq(self.center_freq_1, self.center_freq_2)
        self.sdrplay3_rspduo_0.set_bandwidth(self.samp_rate)
        self.sdrplay3_rspduo_0.set_antenna("Both Tuners")
        self.sdrplay3_rspduo_0.set_gain_modes(False, False)
        self.sdrplay3_rspduo_0.set_gain(self.IF_gain_1, self.IF_gain_2, 'IF')
        self.sdrplay3_rspduo_0.set_gain(self.RF_gain_1, self.RF_gain_2, 'RF')
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


        temp_file_path_1 = DirFuncs.return_temp_file_path(self.chunk_start_time, tag_1)
        pmt_dict_1 = PMTFuncs.get_dict(samp_rate = int(self.samp_rate), center_freq = float(self.center_freq_1), chunk_start_time = self.chunk_start_time)
        self.blocks_file_meta_sink_1 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, temp_file_path_1, self.samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, pmt_dict_1, True)
        self.blocks_file_meta_sink_1.set_unbuffered(False)

        temp_file_path_2 = DirFuncs.return_temp_file_path(self.chunk_start_time, tag_2)
        pmt_dict_2 = PMTFuncs.get_dict(samp_rate = int(self.samp_rate), center_freq = float(self.center_freq_2), chunk_start_time = self.chunk_start_time)
        self.blocks_file_meta_sink_2 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, temp_file_path_2, self.samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, pmt_dict_2, True)
        self.blocks_file_meta_sink_2.set_unbuffered(False)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.sdrplay3_rspduo_0, 0), (self.blocks_file_meta_sink_1, 0))
        self.connect((self.sdrplay3_rspduo_0, 1), (self.blocks_file_meta_sink_2, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rsp_duo_test")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()




def main(tag_1, tag_2, top_block_cls=DuoBatchObserve, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(tag_1, tag_2)

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
    tag_1, tag_2 = Tags.get_tags_from_args()
    #tag_1 will apply the parameters in config_dict to Tuner 1 of the the RSPDuo, similarly for tag_2
    main(tag_1, tag_2)
