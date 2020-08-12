#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.7.13.5
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt, QtCore
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import AISTX
import osmosdr
import sys
import time
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 326531
        self.channel_select = channel_select = 2
        self.bit_rate = bit_rate = 9600

        ##################################################
        # Blocks
        ##################################################
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(100e6, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.digital_gmsk_mod_0_0 = digital.gmsk_mod(
        	samples_per_symbol=int(samp_rate/bit_rate),
        	bt=0.4,
        	verbose=False,
        	log=False,
        )
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=int(samp_rate/bit_rate),
        	bt=0.4,
        	verbose=False,
        	log=False,
        )
        self.blocks_multiply_xx_0_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0_1_0 = blocks.multiply_const_vcc((0.9, ))
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vcc((0.9, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((0.45, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.45, ))
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blks2_selector_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=3,
        	num_outputs=1,
        	input_index=channel_select,
        	output_index=0,
        )
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, 25000, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_SIN_WAVE, -25000, 1, 0)
        self.AISTX_Build_Frame_1 = AISTX.Build_Frame('010100000001101100011001110111011011110000000000000001011110000000000000', True, True)
        self.AISTX_Build_Frame_0 = AISTX.Build_Frame('000100000001101100011001110111011011110000000000000000000000011000111100111100100000101100100000101101000110011010001010010100010000000001000000000000000000000000000000', True, True)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.AISTX_Build_Frame_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.AISTX_Build_Frame_1, 0), (self.digital_gmsk_mod_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.blks2_selector_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blks2_selector_0, 2))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.blks2_selector_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1_0, 0), (self.blks2_selector_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.blocks_multiply_const_vxx_0_1_0, 0))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.digital_gmsk_mod_0_0, 0), (self.blocks_multiply_xx_0_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_channel_select(self):
        return self.channel_select

    def set_channel_select(self, channel_select):
        self.channel_select = channel_select
        self.blks2_selector_0.set_input_index(int(self.channel_select))

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate


def main(top_block_cls=top_block, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
