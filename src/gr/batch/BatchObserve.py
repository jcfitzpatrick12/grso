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

from gnuradio import blocks
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
from gnuradio import qtgui
import pmt

from src.configs import GLOBAL_CONFIG
from src.configs.BatchConfig import load_config
from src.gr.batch.MetaDict import MetaDict  # embedded python module
from src.gr.batch import TimeStamper  # embedded python module

class BatchObserve(gr.top_block, Qt.QWidget):
    def __init__(self, tag):
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

        self.settings = Qt.QSettings("GNU Radio", "BatchObserve")

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

        batch_config = load_config(tag)
        self.samp_rate = batch_config.get_samp_rate()
        self.IF_gain = batch_config.get_IF_gain()
        self.RF_gain = batch_config.get_RF_gain()
        self.center_freq = batch_config.get_center_freq()
        self.chunk_start_time = TimeStamper.return_time_now_as_string()

        ##################################################
        # Blocks
        ##################################################
        self.sdrplay3_rsp1a_0 = sdrplay3.rsp1a(
            '',
            stream_args=sdrplay3.stream_args(
                output_type='fc32',
                channels_size=1
            ),
        )
        self.sdrplay3_rsp1a_0.set_sample_rate(self.samp_rate)
        self.sdrplay3_rsp1a_0.set_center_freq(self.center_freq)
        self.sdrplay3_rsp1a_0.set_bandwidth(self.samp_rate)
        self.sdrplay3_rsp1a_0.set_gain_mode(False)
        self.sdrplay3_rsp1a_0.set_gain(self.IF_gain, 'IF')
        self.sdrplay3_rsp1a_0.set_gain(self.RF_gain, 'RF')
        self.sdrplay3_rsp1a_0.set_freq_corr(0)
        self.sdrplay3_rsp1a_0.set_dc_offset_mode(False)
        self.sdrplay3_rsp1a_0.set_iq_balance_mode(False)
        self.sdrplay3_rsp1a_0.set_agc_setpoint(-30)
        self.sdrplay3_rsp1a_0.set_rf_notch_filter(False)
        self.sdrplay3_rsp1a_0.set_dab_notch_filter(False)
        self.sdrplay3_rsp1a_0.set_biasT(False)
        self.sdrplay3_rsp1a_0.set_debug_mode(False)
        self.sdrplay3_rsp1a_0.set_sample_sequence_gaps_check(False)
        self.sdrplay3_rsp1a_0.set_show_gain_changes(False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, self.samp_rate,True)

        temp_file_path = TimeStamper.return_temp_file_path(self.chunk_start_time, tag)
        
        md = MetaDict()
        meta_dict = md.get_dict(self.samp_rate,self.center_freq,self.chunk_start_time)

        self.blocks_file_meta_sink_0_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, temp_file_path, self.samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, meta_dict, True)
        self.blocks_file_meta_sink_0_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle_0, 0), (self.blocks_file_meta_sink_0_0, 0))
        self.connect((self.sdrplay3_rsp1a_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "BatchObserve")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()



def main(tag, top_block_cls=BatchObserve, options=None):

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

    tb = top_block_cls(tag)

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
        tag = str(sys.argv[1])
    except:
        raise ValueError("Please specify the tag by passing in through the command line.")
    
    if tag not in GLOBAL_CONFIG.defined_tags:
        raise ValueError(f"Please specify a valid tag. Received {tag}, need one of {GLOBAL_CONFIG.defined_tags}")

    main(tag)
