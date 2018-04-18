#!/usr/bin/env python

from scapy.all import *

ap_list = []

def PacketHandler(pkt) :

	if pkt.haslayer(Dot11) :
		if pkt.type == 0 and pkt.subtype == 8 :
			if pkt.addr2 not in ap_list :
				ap_list.append(pkt.addr2)
				channel = int( ord(pkt[Dot11Elt:3].info))
				print("AP MAC: %s with SSID: %s using channel: %s" %(pkt.addr2, pkt.info, int( ord(pkt[Dot11Elt:3].info))))


sniff(iface="wlan0mon", prn = PacketHandler)
