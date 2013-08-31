#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Example NBFM transmitter
# Author: W2XH
# Generated: Tue Aug 13 20:06:35 2013
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx

class bladerf_nfm_tx(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Example NBFM transmitter")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 96e3
        self.xlate_filter_taps = xlate_filter_taps = firdes.low_pass(1, samp_rate, 48000, 5000, firdes.WIN_HAMMING, 6.76)
        self.offset_fine = offset_fine = 0
        self.offset_coarse = offset_coarse = 0
        self.freq = freq = 446.66e6

        ##################################################
        # Blocks
        ##################################################
        _offset_fine_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_fine_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_offset_fine_sizer,
        	value=self.offset_fine,
        	callback=self.set_offset_fine,
        	label="Fine tune",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_fine_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_offset_fine_sizer,
        	value=self.offset_fine,
        	callback=self.set_offset_fine,
        	minimum=-1000,
        	maximum=1000,
        	num_steps=400,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_offset_fine_sizer, 6, 0, 1, 2)
        _offset_coarse_sizer = wx.BoxSizer(wx.VERTICAL)
        self._offset_coarse_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_offset_coarse_sizer,
        	value=self.offset_coarse,
        	callback=self.set_offset_coarse,
        	label="Coarse tune",
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._offset_coarse_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_offset_coarse_sizer,
        	value=self.offset_coarse,
        	callback=self.set_offset_coarse,
        	minimum=-48000,
        	maximum=48000,
        	num_steps=960,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.GridAdd(_offset_coarse_sizer, 6, 2, 1, 2)
        self.osmosdr_sink_0 = osmosdr.sink( args="nchan=" + str(1) + " " + "bladerf=0,fpga=/tmp/hostedx115.rbf" )
        self.osmosdr_sink_0.set_sample_rate(samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(10, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna("", 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)
          
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, (xlate_filter_taps), -(offset_coarse+offset_fine), samp_rate)
        self.blocks_wavfile_source_0 = blocks.wavfile_source("/tmp/w2xh_id.wav", True)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=int(samp_rate/2),
        	quad_rate=int(samp_rate),
        	tau=75e-6,
        	max_dev=5e3,
        )

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_nbfm_tx_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_nbfm_tx_0, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_xlate_filter_taps(firdes.low_pass(1, self.samp_rate, 48000, 5000, firdes.WIN_HAMMING, 6.76))
        self.osmosdr_sink_0.set_sample_rate(self.samp_rate)

    def get_xlate_filter_taps(self):
        return self.xlate_filter_taps

    def set_xlate_filter_taps(self, xlate_filter_taps):
        self.xlate_filter_taps = xlate_filter_taps
        self.freq_xlating_fir_filter_xxx_0.set_taps((self.xlate_filter_taps))

    def get_offset_fine(self):
        return self.offset_fine

    def set_offset_fine(self, offset_fine):
        self.offset_fine = offset_fine
        self._offset_fine_slider.set_value(self.offset_fine)
        self._offset_fine_text_box.set_value(self.offset_fine)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.offset_coarse+self.offset_fine))

    def get_offset_coarse(self):
        return self.offset_coarse

    def set_offset_coarse(self, offset_coarse):
        self.offset_coarse = offset_coarse
        self._offset_coarse_slider.set_value(self.offset_coarse)
        self._offset_coarse_text_box.set_value(self.offset_coarse)
        self.freq_xlating_fir_filter_xxx_0.set_center_freq(-(self.offset_coarse+self.offset_fine))

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = bladerf_nfm_tx()
    tb.Start(True)
    tb.Wait()

