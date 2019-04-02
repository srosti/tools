#!/usr/bin/env python3
"""
    Copyright © 2016 Cradlepoint, Inc. <www.cradlepoint.com>.  All rights reserved.

    This file contains confidential information of Cradlepoint, Inc. and your
    use of this file is subject to the Cradlepoint Software License Agreement
    distributed with this file. Unauthorized reproduction or distribution of
    this file is subject to civil and criminal penalties.

    Desc:

"""
#
# davep 20160906 ;  tinker with Requests library and WiFi

import sys
import logging

logger = logging.getLogger("wifi")

from .webapi import WebAPI, RouterConfig, RouterStatus, want_array

# valid "authmode" from config_dtd.json because I keep forgetting the names
authmode = {
#	firmware_name: human_name
	"none": "None",
	"wepauto": "WEP Auto",
	"wepopen": "WEP Open",
	"wepshared": "WEP Shared",
	"wpa1psk": "WPA1 Personal",
	"wpa1": "WPA1 Enterprise",
	"wpa2psk": "WPA2 Personal",
	"wpa2": "WPA2 Enterprise",
	"wpa1wpa2psk": "WPA1 & WPA2 Personal",
	"wpa1wpa2": "WPA1 & WPA2 Enterprise",
}

# categorize auth modes for convenience of test scripts
wep_auth_modes = ("wepauto", "wepopen", "wepshared")
wpa_psk_modes = ( "wpa1psk", "wpa2psk", "wpa1wpa2psk")
wpa_ent_modes = ( "wpa1", "wpa2", "wpa1wpa2")

# valid phymhz because there's a new kid in town: 20/40/80 Mhz
#
phymhz = {
	0: "20",
	1: "20/40 Auto",
	2: "20/40/80 Auto",
}

# valid "wpacipher" from config_dtd.json because I keep forgetting the names
wpacipher = {
#	firmware_name: human_name
	"tkip": "TKIP",
	"tkipaes": "TKIP & AES",
	"aes": "AES"
}

class WiFiRadioBSSConfig(RouterConfig):
	path = "/api/config/wlan/radio/{0.radio_idx}/bss/{0.idx}/{1}"

	def __init__(self, api, radio_idx, bss_idx):
		super().__init__(api)
		self.__dict__["radio_idx"] = radio_idx
		self.__dict__["idx"] = bss_idx

	def __str__(self):
		return "<" + super().__str__() + " radio={} bss={}>".format(self.radio_idx, self.idx)


class RadioMixin(object):
	def __str__(self):
		return "<" + super().__str__() + " radio={}>".format(self.idx)

class WiFiRadioConfig(RadioMixin, RouterConfig):
	path = "/api/config/wlan/radio/{0.idx}/{1}"

	def __init__(self, api, radio_idx):
		super().__init__(api)
		self.__dict__["idx"] = radio_idx

		# what's the plural of bss!?
		self.__dict__["bss"] = []

		# how many BSS does this radio have?
		path = "/api/shallow/config/wlan/radio/{}/bss".format(self.idx)
		bss_list = want_array(self.api.get(path))
		for bss_idx, bss in enumerate(bss_list):
			logger.debug("{} found bss idx={}".format(str(self), bss_idx))
			self.bss.append(WiFiRadioBSSConfig(self.api, self.idx, bss_idx))

class WiFiConfig(RouterConfig):
	path = "/api/config/wlan/{1}"

	def __init__(self, api):
		super().__init__(api)

		self.__dict__["radios"] = []

		# how many radios do we have?
		path = "/api/shallow/config/wlan/radio"
		radio_list = want_array(self.api.get(path))
		for radio_idx, radio in enumerate(radio_list):
			logger.debug("wifi {} found radio idx={}".format(str(self), radio_idx))
			self.radios.append(WiFiRadioConfig(self.api, radio_idx))

	def __str__(self):
		return "<" + super().__str__() + " radios={}>".format(len(self.radios))

def get_num_radios(conn):
	# how many radios do we have?
	path = "/api/shallow/config/wlan/radio"
	radios = conn.get(path)
	num_radios = len(radios)
	return num_radios

def main():
	import wifi
	#
	# This is some simple test code that peeks around in various wifi config.
	# No writes are performed.
	#
	args = cmdline.CommandLine()
	logging.basicConfig(level=args.loglevel)
	conn = WebAPI(verify=args.cacert, **args.device)

	# putter around with WiFi-as-WAN profiles
	wwan = WWANConfig(conn)
	for radio in wwan.radios:
		print("radio={} mode={}".format(radio, radio.mode))
		for profile in radio.profiles:
			print("profile=", profile)
			print("profile ssid=\"{}\" enabled={} authmode={}".format(profile.ssid, profile.enabled, profile.authmode))

	# peek around in config
	wlan = WiFiConfig(conn)
	print("wlan=", wlan)
	print("{} verbosity={}".format(wlan, wlan.wlan_verbosity))
	for radio in wlan.radios:
		print("radio=",radio)
		print("radio={} enabled={} txpower={}".format(radio.idx, radio.enabled, radio.txpower))
		for bss in radio.bss:
			print("bss=", bss)
			print("{} ssid=\"{}\" enabled={}".format(bss, bss.ssid, bss.enabled))
			print("{} ssid=\"{}\" radius={},{},{}".format(bss, bss.ssid, bss.radius0ip, bss.radius0port, bss.radius1ip))

if __name__=='__main__':
#	logging.basicConfig(level=logging.DEBUG)
#	logging.basicConfig(level=logging.INFO)
#	logging.basicConfig(level=logging.ERROR)

	main()
