#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Example NBFM transmitter
# Author: W2XH
# Generated: Sun Sep  1 10:17:07 2013
##################################################

from gnuradio import analog
from gnuradio import blks2
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import forms
from grc_gnuradio import blks2 as grc_blks2
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
		self.selector_input = selector_input = 0
		self.samp_rate = samp_rate = 96e3
		self.offset_fine = offset_fine = 0
		self.offset_coarse = offset_coarse = 0
		self.interp = interp = 4
		self.freq = freq = 446.66e6

		##################################################
		# Blocks
		##################################################
		self._selector_input_chooser = forms.button(
			parent=self.GetWin(),
			value=self.selector_input,
			callback=self.set_selector_input,
			label="Audio",
			choices=[0, 1],
			labels=["wav", "tone"],
		)
		self.Add(self._selector_input_chooser)
		self.osmosdr_sink_c_0 = osmosdr.sink_c( args="nchan=" + str(1) + " " + "bladerf=0" )
		self.osmosdr_sink_c_0.set_sample_rate(samp_rate*interp)
		self.osmosdr_sink_c_0.set_center_freq(freq, 0)
		self.osmosdr_sink_c_0.set_freq_corr(0, 0)
		self.osmosdr_sink_c_0.set_gain(0, 0)
		self.osmosdr_sink_c_0.set_if_gain(0, 0)
		self.osmosdr_sink_c_0.set_bb_gain(0, 0)
		self.osmosdr_sink_c_0.set_antenna("", 0)
		self.osmosdr_sink_c_0.set_bandwidth(1.5e6, 0)
		  
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
		self.low_pass_filter_0 = gr.interp_fir_filter_ccf(interp, firdes.low_pass(
			1, samp_rate, 5e3, 1.5e3, firdes.WIN_HAMMING, 6.76))
		self.blocks_wavfile_source_0 = blocks.wavfile_source("/home/rtucker/Dropbox/tmp/w2xh_id.wav", True)
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_float*1, samp_rate/2)
		self.blks2_selector_0 = grc_blks2.selector(
			item_size=gr.sizeof_float*1,
			num_inputs=2,
			num_outputs=1,
			input_index=selector_input,
			output_index=0,
		)
		self.blks2_nbfm_tx_0 = blks2.nbfm_tx(
			audio_rate=int(48e3),
			quad_rate=int(samp_rate),
			tau=75e-6,
			max_dev=5e3,
		)
		self.analog_sig_source_x_0 = analog.sig_source_f(samp_rate/2, analog.GR_SIN_WAVE, 1000, 1, 0)

		##################################################
		# Connections
		##################################################
		self.connect((self.analog_sig_source_x_0, 0), (self.blks2_selector_0, 1))
		self.connect((self.blocks_throttle_0, 0), (self.blks2_nbfm_tx_0, 0))
		self.connect((self.blks2_nbfm_tx_0, 0), (self.low_pass_filter_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.osmosdr_sink_c_0, 0))
		self.connect((self.blocks_wavfile_source_0, 0), (self.blks2_selector_0, 0))
		self.connect((self.blks2_selector_0, 0), (self.blocks_throttle_0, 0))


	def get_selector_input(self):
		return self.selector_input

	def set_selector_input(self, selector_input):
		self.selector_input = selector_input
		self._selector_input_chooser.set_value(self.selector_input)
		self.blks2_selector_0.set_input_index(int(self.selector_input))

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.osmosdr_sink_c_0.set_sample_rate(self.samp_rate*self.interp)
		self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate/2)
		self.blocks_throttle_0.set_sample_rate(self.samp_rate/2)
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 5e3, 1.5e3, firdes.WIN_HAMMING, 6.76))

	def get_offset_fine(self):
		return self.offset_fine

	def set_offset_fine(self, offset_fine):
		self.offset_fine = offset_fine
		self._offset_fine_slider.set_value(self.offset_fine)
		self._offset_fine_text_box.set_value(self.offset_fine)

	def get_offset_coarse(self):
		return self.offset_coarse

	def set_offset_coarse(self, offset_coarse):
		self.offset_coarse = offset_coarse
		self._offset_coarse_slider.set_value(self.offset_coarse)
		self._offset_coarse_text_box.set_value(self.offset_coarse)

	def get_interp(self):
		return self.interp

	def set_interp(self, interp):
		self.interp = interp
		self.osmosdr_sink_c_0.set_sample_rate(self.samp_rate*self.interp)

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.osmosdr_sink_c_0.set_center_freq(self.freq, 0)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = bladerf_nfm_tx()
	tb.Run(True)

