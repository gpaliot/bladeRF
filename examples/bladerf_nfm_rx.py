#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: bladeRF NBFM Receiver
# Author: W2XH
# Description: Dual-channel Narrowband FM receiver for the nuand BladeRF
# Generated: Sun Sep  1 13:54:54 2013
##################################################

from gnuradio import analog
from gnuradio import audio
from gnuradio import blks2
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.gr import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import wx

class bladerf_nfm_rx(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="bladeRF NBFM Receiver")
		_icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
		self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

		##################################################
		# Variables
		##################################################
		self.freq_sec = freq_sec = 444.400e6
		self.freq = freq = 444.250e6
		self.tune_freq = tune_freq = (freq + freq_sec) / 2.0
		self.samp_rate = samp_rate = int(96e3*4)
		self.offset_fine_sec = offset_fine_sec = 0
		self.offset_fine = offset_fine = 0
		self.offset_coarse_sec = offset_coarse_sec = 0
		self.offset_coarse = offset_coarse = 0
		self.shift_sec = shift_sec = min(samp_rate/2, max(-samp_rate/2, (freq_sec-tune_freq)+(offset_coarse_sec+offset_fine_sec)))
		self.shift_main = shift_main = min(samp_rate/2, max(-samp_rate/2, (freq-tune_freq)+(offset_coarse+offset_fine)))
		self.xlate_filter_taps = xlate_filter_taps = firdes.low_pass(1, samp_rate, samp_rate/2, 5000, firdes.WIN_HAMMING, 6.76)
		self.width = width = 10000
		self.tune_freq_show = tune_freq_show = tune_freq
		self.trans = trans = 1500
		self.sql_lev = sql_lev = -40
		self.rx_freq_sec = rx_freq_sec = tune_freq+shift_sec
		self.rx_freq = rx_freq = tune_freq+shift_main
		self.rf_gain = rf_gain = 20
		self.display_selector = display_selector = 1
		self.cheesy_greeting = cheesy_greeting = "Running"
		self.af_gain = af_gain = 5

		##################################################
		# Blocks
		##################################################
		_width_sizer = wx.BoxSizer(wx.VERTICAL)
		self._width_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_width_sizer,
			value=self.width,
			callback=self.set_width,
			label="Filter",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._width_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_width_sizer,
			value=self.width,
			callback=self.set_width,
			minimum=2000,
			maximum=40000,
			num_steps=760,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_width_sizer, 8, 0, 1, 1)
		_trans_sizer = wx.BoxSizer(wx.VERTICAL)
		self._trans_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_trans_sizer,
			value=self.trans,
			callback=self.set_trans,
			label="Trans",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._trans_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_trans_sizer,
			value=self.trans,
			callback=self.set_trans,
			minimum=500,
			maximum=5000,
			num_steps=900,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_trans_sizer, 8, 1, 1, 2)
		_sql_lev_sizer = wx.BoxSizer(wx.VERTICAL)
		self._sql_lev_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_sql_lev_sizer,
			value=self.sql_lev,
			callback=self.set_sql_lev,
			label="SQL",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._sql_lev_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_sql_lev_sizer,
			value=self.sql_lev,
			callback=self.set_sql_lev,
			minimum=-80,
			maximum=0,
			num_steps=500,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_sql_lev_sizer, 9, 1, 1, 2)
		self._samp_rate_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.samp_rate,
			callback=self.set_samp_rate,
			label="Sample Rate",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._samp_rate_static_text, 5, 2, 1, 1)
		_rf_gain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._rf_gain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_rf_gain_sizer,
			value=self.rf_gain,
			callback=self.set_rf_gain,
			label="RF",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._rf_gain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_rf_gain_sizer,
			value=self.rf_gain,
			callback=self.set_rf_gain,
			minimum=-5,
			maximum=30,
			num_steps=35,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_rf_gain_sizer, 9, 0, 1, 1)
		self._display_selector_chooser = forms.drop_down(
			parent=self.GetWin(),
			value=self.display_selector,
			callback=self.set_display_selector,
			label="Spectrum",
			choices=[0, 1],
			labels=['Baseband','RF'],
		)
		self.GridAdd(self._display_selector_chooser, 5, 0, 1, 1)
		_af_gain_sizer = wx.BoxSizer(wx.VERTICAL)
		self._af_gain_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_af_gain_sizer,
			value=self.af_gain,
			callback=self.set_af_gain,
			label="VOL",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._af_gain_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_af_gain_sizer,
			value=self.af_gain,
			callback=self.set_af_gain,
			minimum=0,
			maximum=11,
			num_steps=50,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_af_gain_sizer, 9, 3, 1, 1)
		self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
			self.GetWin(),
			baseband_freq=tune_freq*display_selector,
			dynamic_range=70,
			ref_level=0,
			ref_scale=2.0,
			sample_rate=samp_rate,
			fft_size=512,
			fft_rate=15,
			average=False,
			avg_alpha=None,
			title="Waterfall Plot",
			size=(500, 300),
		)
		self.GridAdd(self.wxgui_waterfallsink2_0.win, 0, 4, 5, 4)
		self._tune_freq_show_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.tune_freq_show,
			callback=self.set_tune_freq_show,
			label="Center Freq",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._tune_freq_show_static_text, 5, 3, 1, 1)
		self._rx_freq_sec_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.rx_freq_sec,
			callback=self.set_rx_freq_sec,
			label="Sec RX",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._rx_freq_sec_static_text, 7, 3, 1, 1)
		self._rx_freq_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.rx_freq,
			callback=self.set_rx_freq,
			label="Main RX",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._rx_freq_static_text, 6, 3, 1, 1)
		self.osmosdr_source_c_0 = osmosdr.source_c( args="nchan=" + str(1) + " " + "" )
		self.osmosdr_source_c_0.set_sample_rate(samp_rate)
		self.osmosdr_source_c_0.set_center_freq(tune_freq, 0)
		self.osmosdr_source_c_0.set_freq_corr(0, 0)
		self.osmosdr_source_c_0.set_dc_offset_mode(0, 0)
		self.osmosdr_source_c_0.set_iq_balance_mode(0, 0)
		self.osmosdr_source_c_0.set_gain_mode(0, 0)
		self.osmosdr_source_c_0.set_gain(6, 0)
		self.osmosdr_source_c_0.set_if_gain(rf_gain, 0)
		self.osmosdr_source_c_0.set_bb_gain(20, 0)
		self.osmosdr_source_c_0.set_antenna("", 0)
		self.osmosdr_source_c_0.set_bandwidth(0, 0)
		  
		_offset_fine_sec_sizer = wx.BoxSizer(wx.VERTICAL)
		self._offset_fine_sec_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_offset_fine_sec_sizer,
			value=self.offset_fine_sec,
			callback=self.set_offset_fine_sec,
			label="Fine tune",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._offset_fine_sec_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_offset_fine_sec_sizer,
			value=self.offset_fine_sec,
			callback=self.set_offset_fine_sec,
			minimum=-1000,
			maximum=1000,
			num_steps=400,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_offset_fine_sec_sizer, 7, 2, 1, 1)
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
		self.GridAdd(_offset_fine_sizer, 6, 2, 1, 1)
		_offset_coarse_sec_sizer = wx.BoxSizer(wx.VERTICAL)
		self._offset_coarse_sec_text_box = forms.text_box(
			parent=self.GetWin(),
			sizer=_offset_coarse_sec_sizer,
			value=self.offset_coarse_sec,
			callback=self.set_offset_coarse_sec,
			label="Coarse tune",
			converter=forms.float_converter(),
			proportion=0,
		)
		self._offset_coarse_sec_slider = forms.slider(
			parent=self.GetWin(),
			sizer=_offset_coarse_sec_sizer,
			value=self.offset_coarse_sec,
			callback=self.set_offset_coarse_sec,
			minimum=-48000,
			maximum=48000,
			num_steps=960,
			style=wx.SL_HORIZONTAL,
			cast=float,
			proportion=1,
		)
		self.GridAdd(_offset_coarse_sec_sizer, 7, 1, 1, 1)
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
		self.GridAdd(_offset_coarse_sizer, 6, 1, 1, 1)
		self.low_pass_filter_0 = gr.fir_filter_ccf(1, firdes.low_pass(
			1, samp_rate, width/2, trans, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter = gr.fir_filter_ccf(1, firdes.low_pass(
			1, samp_rate, width/2, trans, firdes.WIN_HAMMING, 6.76))
		self.freq_xlating_fir_filter_sec = filter.freq_xlating_fir_filter_ccc(1, (xlate_filter_taps), shift_sec, samp_rate)
		self.freq_xlating_fir_filter_main = filter.freq_xlating_fir_filter_ccc(1, (xlate_filter_taps), shift_main, samp_rate)
		self._freq_sec_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.freq_sec,
			callback=self.set_freq_sec,
			label="Sec Freq",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._freq_sec_text_box, 7, 0, 1, 1)
		self._freq_text_box = forms.text_box(
			parent=self.GetWin(),
			value=self.freq,
			callback=self.set_freq,
			label="Main Freq",
			converter=forms.float_converter(),
		)
		self.GridAdd(self._freq_text_box, 6, 0, 1, 1)
		self.fftsink = fftsink2.fft_sink_c(
			self.GetWin(),
			baseband_freq=tune_freq*display_selector,
			y_per_div=10,
			y_divs=10,
			ref_level=20,
			ref_scale=1.0,
			sample_rate=samp_rate,
			fft_size=512,
			fft_rate=15,
			average=True,
			avg_alpha=0.5,
			title="FFT",
			peak_hold=False,
			size=(500, 300),
		)
		self.GridAdd(self.fftsink.win, 0, 0, 5, 4)
		self._cheesy_greeting_static_text = forms.static_text(
			parent=self.GetWin(),
			value=self.cheesy_greeting,
			callback=self.set_cheesy_greeting,
			label="bladeRF Dual NBFM Receiver by W2XH",
			converter=forms.str_converter(),
		)
		self.GridAdd(self._cheesy_greeting_static_text, 10, 0, 1, 4)
		self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate)
		self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_vff((af_gain, ))
		self.blocks_multiply_const_vxx_1 = blocks.multiply_const_vff((af_gain, ))
		self.blks2_nbfm_rx_0_0 = blks2.nbfm_rx(
			audio_rate=48000,
			quad_rate=samp_rate,
			tau=75e-6,
			max_dev=5e3,
		)
		self.blks2_nbfm_rx_0 = blks2.nbfm_rx(
			audio_rate=48000,
			quad_rate=samp_rate,
			tau=75e-6,
			max_dev=5e3,
		)
		self.audio_sink = audio.sink(48000, "", True)
		self.analog_simple_squelch_cc_0_0 = analog.simple_squelch_cc(sql_lev, 1)
		self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(sql_lev, 1)

		##################################################
		# Connections
		##################################################
		self.connect((self.blks2_nbfm_rx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
		self.connect((self.analog_simple_squelch_cc_0, 0), (self.blks2_nbfm_rx_0, 0))
		self.connect((self.low_pass_filter, 0), (self.analog_simple_squelch_cc_0, 0))
		self.connect((self.blocks_multiply_const_vxx_1, 0), (self.audio_sink, 0))
		self.connect((self.blks2_nbfm_rx_0_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
		self.connect((self.analog_simple_squelch_cc_0_0, 0), (self.blks2_nbfm_rx_0_0, 0))
		self.connect((self.low_pass_filter_0, 0), (self.analog_simple_squelch_cc_0_0, 0))
		self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.audio_sink, 1))
		self.connect((self.freq_xlating_fir_filter_sec, 0), (self.low_pass_filter_0, 0))
		self.connect((self.freq_xlating_fir_filter_main, 0), (self.low_pass_filter, 0))
		self.connect((self.osmosdr_source_c_0, 0), (self.blocks_throttle_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_main, 0))
		self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_sec, 0))
		self.connect((self.blocks_throttle_0, 0), (self.wxgui_waterfallsink2_0, 0))
		self.connect((self.blocks_throttle_0, 0), (self.fftsink, 0))


	def get_freq_sec(self):
		return self.freq_sec

	def set_freq_sec(self, freq_sec):
		self.freq_sec = freq_sec
		self.set_tune_freq((self.freq + self.freq_sec) / 2.0)
		self._freq_sec_text_box.set_value(self.freq_sec)
		self.set_shift_sec(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq_sec-self.tune_freq)+(self.offset_coarse_sec+self.offset_fine_sec))))

	def get_freq(self):
		return self.freq

	def set_freq(self, freq):
		self.freq = freq
		self.set_tune_freq((self.freq + self.freq_sec) / 2.0)
		self._freq_text_box.set_value(self.freq)
		self.set_shift_main(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq-self.tune_freq)+(self.offset_coarse+self.offset_fine))))

	def get_tune_freq(self):
		return self.tune_freq

	def set_tune_freq(self, tune_freq):
		self.tune_freq = tune_freq
		self.fftsink.set_baseband_freq(self.tune_freq*self.display_selector)
		self.osmosdr_source_c_0.set_center_freq(self.tune_freq, 0)
		self.wxgui_waterfallsink2_0.set_baseband_freq(self.tune_freq*self.display_selector)
		self.set_rx_freq(self.tune_freq+self.shift_main)
		self.set_rx_freq_sec(self.tune_freq+self.shift_sec)
		self.set_shift_sec(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq_sec-self.tune_freq)+(self.offset_coarse_sec+self.offset_fine_sec))))
		self.set_shift_main(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq-self.tune_freq)+(self.offset_coarse+self.offset_fine))))
		self.set_tune_freq_show(self.tune_freq)

	def get_samp_rate(self):
		return self.samp_rate

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.low_pass_filter.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))
		self.set_xlate_filter_taps(firdes.low_pass(1, self.samp_rate, self.samp_rate/2, 5000, firdes.WIN_HAMMING, 6.76))
		self.fftsink.set_sample_rate(self.samp_rate)
		self.blocks_throttle_0.set_sample_rate(self.samp_rate)
		self.osmosdr_source_c_0.set_sample_rate(self.samp_rate)
		self.wxgui_waterfallsink2_0.set_sample_rate(self.samp_rate)
		self.set_shift_sec(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq_sec-self.tune_freq)+(self.offset_coarse_sec+self.offset_fine_sec))))
		self.set_shift_main(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq-self.tune_freq)+(self.offset_coarse+self.offset_fine))))
		self._samp_rate_static_text.set_value(self.samp_rate)

	def get_offset_fine_sec(self):
		return self.offset_fine_sec

	def set_offset_fine_sec(self, offset_fine_sec):
		self.offset_fine_sec = offset_fine_sec
		self._offset_fine_sec_slider.set_value(self.offset_fine_sec)
		self._offset_fine_sec_text_box.set_value(self.offset_fine_sec)
		self.set_shift_sec(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq_sec-self.tune_freq)+(self.offset_coarse_sec+self.offset_fine_sec))))

	def get_offset_fine(self):
		return self.offset_fine

	def set_offset_fine(self, offset_fine):
		self.offset_fine = offset_fine
		self._offset_fine_slider.set_value(self.offset_fine)
		self._offset_fine_text_box.set_value(self.offset_fine)
		self.set_shift_main(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq-self.tune_freq)+(self.offset_coarse+self.offset_fine))))

	def get_offset_coarse_sec(self):
		return self.offset_coarse_sec

	def set_offset_coarse_sec(self, offset_coarse_sec):
		self.offset_coarse_sec = offset_coarse_sec
		self._offset_coarse_sec_slider.set_value(self.offset_coarse_sec)
		self._offset_coarse_sec_text_box.set_value(self.offset_coarse_sec)
		self.set_shift_sec(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq_sec-self.tune_freq)+(self.offset_coarse_sec+self.offset_fine_sec))))

	def get_offset_coarse(self):
		return self.offset_coarse

	def set_offset_coarse(self, offset_coarse):
		self.offset_coarse = offset_coarse
		self._offset_coarse_slider.set_value(self.offset_coarse)
		self._offset_coarse_text_box.set_value(self.offset_coarse)
		self.set_shift_main(min(self.samp_rate/2, max(-self.samp_rate/2, (self.freq-self.tune_freq)+(self.offset_coarse+self.offset_fine))))

	def get_shift_sec(self):
		return self.shift_sec

	def set_shift_sec(self, shift_sec):
		self.shift_sec = shift_sec
		self.freq_xlating_fir_filter_sec.set_center_freq(self.shift_sec)
		self.set_rx_freq_sec(self.tune_freq+self.shift_sec)

	def get_shift_main(self):
		return self.shift_main

	def set_shift_main(self, shift_main):
		self.shift_main = shift_main
		self.freq_xlating_fir_filter_main.set_center_freq(self.shift_main)
		self.set_rx_freq(self.tune_freq+self.shift_main)

	def get_xlate_filter_taps(self):
		return self.xlate_filter_taps

	def set_xlate_filter_taps(self, xlate_filter_taps):
		self.xlate_filter_taps = xlate_filter_taps
		self.freq_xlating_fir_filter_sec.set_taps((self.xlate_filter_taps))
		self.freq_xlating_fir_filter_main.set_taps((self.xlate_filter_taps))

	def get_width(self):
		return self.width

	def set_width(self, width):
		self.width = width
		self.low_pass_filter.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))
		self._width_slider.set_value(self.width)
		self._width_text_box.set_value(self.width)

	def get_tune_freq_show(self):
		return self.tune_freq_show

	def set_tune_freq_show(self, tune_freq_show):
		self.tune_freq_show = tune_freq_show
		self._tune_freq_show_static_text.set_value(self.tune_freq_show)

	def get_trans(self):
		return self.trans

	def set_trans(self, trans):
		self.trans = trans
		self.low_pass_filter.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))
		self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.width/2, self.trans, firdes.WIN_HAMMING, 6.76))
		self._trans_slider.set_value(self.trans)
		self._trans_text_box.set_value(self.trans)

	def get_sql_lev(self):
		return self.sql_lev

	def set_sql_lev(self, sql_lev):
		self.sql_lev = sql_lev
		self.analog_simple_squelch_cc_0.set_threshold(self.sql_lev)
		self.analog_simple_squelch_cc_0_0.set_threshold(self.sql_lev)
		self._sql_lev_slider.set_value(self.sql_lev)
		self._sql_lev_text_box.set_value(self.sql_lev)

	def get_rx_freq_sec(self):
		return self.rx_freq_sec

	def set_rx_freq_sec(self, rx_freq_sec):
		self.rx_freq_sec = rx_freq_sec
		self._rx_freq_sec_static_text.set_value(self.rx_freq_sec)

	def get_rx_freq(self):
		return self.rx_freq

	def set_rx_freq(self, rx_freq):
		self.rx_freq = rx_freq
		self._rx_freq_static_text.set_value(self.rx_freq)

	def get_rf_gain(self):
		return self.rf_gain

	def set_rf_gain(self, rf_gain):
		self.rf_gain = rf_gain
		self._rf_gain_slider.set_value(self.rf_gain)
		self._rf_gain_text_box.set_value(self.rf_gain)
		self.osmosdr_source_c_0.set_if_gain(self.rf_gain, 0)

	def get_display_selector(self):
		return self.display_selector

	def set_display_selector(self, display_selector):
		self.display_selector = display_selector
		self._display_selector_chooser.set_value(self.display_selector)
		self.fftsink.set_baseband_freq(self.tune_freq*self.display_selector)
		self.wxgui_waterfallsink2_0.set_baseband_freq(self.tune_freq*self.display_selector)

	def get_cheesy_greeting(self):
		return self.cheesy_greeting

	def set_cheesy_greeting(self, cheesy_greeting):
		self.cheesy_greeting = cheesy_greeting
		self._cheesy_greeting_static_text.set_value(self.cheesy_greeting)

	def get_af_gain(self):
		return self.af_gain

	def set_af_gain(self, af_gain):
		self.af_gain = af_gain
		self.blocks_multiply_const_vxx_1.set_k((self.af_gain, ))
		self.blocks_multiply_const_vxx_1_0.set_k((self.af_gain, ))
		self._af_gain_slider.set_value(self.af_gain)
		self._af_gain_text_box.set_value(self.af_gain)

if __name__ == '__main__':
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	if gr.enable_realtime_scheduling() != gr.RT_OK:
		print "Error: failed to enable realtime scheduling."
	tb = bladerf_nfm_rx()
	tb.Run(True)

