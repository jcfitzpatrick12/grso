#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.8.0

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, blocks
import pmt
from gnuradio import soapy
import observeCollect_pmtDictMaker as pmtDictMaker  # embedded python module
import observeCollect_timeStamper as timeStamper  # embedded python module



class observeCollect(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
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

        self.settings = Qt.QSettings("GNU Radio", "observeCollect")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 3e6
        self.pseudo_start_time = pseudo_start_time = timeStamper.timeStamper().returnDatetimeNowString()
        self.center_freq = center_freq = 40e6

        ##################################################
        # Blocks
        ##################################################

        self.soapy_sdrplay_source_0 = None
        _agc_setpoint = int(0)
        _agc_setpoint = max(min(_agc_setpoint, -20), -70)

        dev = 'driver=sdrplay'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        def _set_soapy_sdrplay_source_0_gain_mode(channel, agc):
            self.soapy_sdrplay_source_0.set_gain_mode(channel, agc)
            if not agc:
                self.set_soapy_sdrplay_source_0_gain(channel, self._soapy_sdrplay_source_0_gain_value)
        self.set_soapy_sdrplay_source_0_gain_mode = _set_soapy_sdrplay_source_0_gain_mode
        self._soapy_sdrplay_source_0_gain_value = 30

        def _set_soapy_sdrplay_source_0_gain(channel, gain):
            self._soapy_sdrplay_source_0_gain_value = gain
            if not self.soapy_sdrplay_source_0.get_gain_mode(channel):
                self.soapy_sdrplay_source_0.set_gain(channel, 'IFGR', min(max(59 - gain, 20), 59))
        self.set_soapy_sdrplay_source_0_gain = _set_soapy_sdrplay_source_0_gain

        def _set_soapy_sdrplay_source_0_lna_state(channel, lna_state):
                self.soapy_sdrplay_source_0.set_gain(channel, 'RFGR', min(max(lna_state, 0), 9))
        self.set_soapy_sdrplay_source_0_lna_state = _set_soapy_sdrplay_source_0_lna_state

        self.soapy_sdrplay_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_sdrplay_source_0.set_sample_rate(0, samp_rate)
        self.soapy_sdrplay_source_0.set_bandwidth(0, samp_rate)
        self.soapy_sdrplay_source_0.set_antenna(0, 'RX')
        self.soapy_sdrplay_source_0.set_frequency(0, center_freq)
        self.soapy_sdrplay_source_0.set_frequency_correction(0, 0)
        # biasT_ctrl is not always available and leaving it blank avoids errors
        if '' != '':
            self.soapy_sdrplay_source_0.write_setting('biasT_ctrl', )
        self.soapy_sdrplay_source_0.write_setting('agc_setpoint', 0)
        self.set_soapy_sdrplay_source_0_gain_mode(0, False)
        self.set_soapy_sdrplay_source_0_gain(0, 30)
        self.set_soapy_sdrplay_source_0_lna_state(0, 1)
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                (samp_rate/2),
                3e3,
                window.WIN_HAMMING,
                6.76))
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_gr_complex*1, samp_rate, True, 0 if "auto" == "auto" else max( int(float(0.1) * samp_rate) if "auto" == "time" else int(0.1), 1) )
        self.blocks_file_meta_sink_0_0 = blocks.file_meta_sink(gr.sizeof_gr_complex*1, timeStamper.timeStamper().returnFilePath(pseudo_start_time), samp_rate, 1, blocks.GR_FILE_FLOAT, True, 1000000, pmtDictMaker.BuildDict().GetDict(samp_rate,center_freq,pseudo_start_time), True)
        self.blocks_file_meta_sink_0_0.set_unbuffered(False)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_throttle2_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_file_meta_sink_0_0, 0))
        self.connect((self.soapy_sdrplay_source_0, 0), (self.blocks_throttle2_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "observeCollect")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle2_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, (self.samp_rate/2), 3e3, window.WIN_HAMMING, 6.76))
        self.soapy_sdrplay_source_0.set_sample_rate(0, self.samp_rate)
        self.soapy_sdrplay_source_0.set_bandwidth(0, self.samp_rate)

    def get_pseudo_start_time(self):
        return self.pseudo_start_time

    def set_pseudo_start_time(self, pseudo_start_time):
        self.pseudo_start_time = pseudo_start_time
        self.blocks_file_meta_sink_0_0.open(timeStamper.timeStamper().returnFilePath(self.pseudo_start_time))

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.soapy_sdrplay_source_0.set_frequency(0, self.center_freq)




def main(top_block_cls=observeCollect, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

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
    main()
