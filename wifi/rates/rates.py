#!/usr/bin/env python

# import scapy module
import scapy.all as scapy
import os as os
import binascii

ap=[]
packets=[]

rates_dict = {
	'1' : '\x82',
	'2' : '\x84',
	'3' : '\x8b',
	'11' : '\x96',
	'6' : '\x0c',
	'9' : '\x12',
	'12' : '\x18',
	'18' : '\x24',
	'24' : '0',
	'36' :'H',
	'48' : '`',
	'54' : 'l'
}

# Extracted Packet Format 
Pkt_Info = """
---------------[ Packet Captured ]-----------------------
 Subtype  : {}   
 Address 1  : {} | Address 2 : {} [BSSID] 
 Address 3  : {} | Address 4 : {} 
 AP   : {} [SSID]
"""
 
def PacketHandler(pkt):
	if pkt.haslayer(scapy.Dot11Elt) and pkt.type == 0 and pkt.subtype == 8:
		if pkt.addr2 not in ap:
			ssid = pkt.payload.payload.payload.info
			ap.append(pkt.addr2)
			packets.append(pkt)
			#print(Pkt_Info.format(pkt.subtype,pkt.addr1, pkt.addr2, pkt.addr3, pkt.addr4, pkt.info))
			rates = None
			extended_rates = None
			if ssid == 'AP22-f36':
				print("ssid = " + ssid)
				get_rates(pkt)

def get_rates(pkt):
	while pkt.payload:
		# Basic Rates layer is in ID=1
		if pkt.ID == 1:
			rates = pkt.info
#			import pdb; pdb.set_trace()
#			print(rates)
#			print(binascii.hexlify(rates))
		if pkt.ID == 50:
			#extended_rates = pkt.info
			rates = rates + pkt.info
#				print(binascii.hexlify(extended_rates))
#				import pdb; pdb.set_trace()
			pkt = pkt.payload
				#rates = int(binascii.hexlify(pkt.payload.payload.payload.payload.info))

	# Check which rates are enabled
	for rate in rates:
		for index, byte in rates_dict.iteritems():
			if byte == rate:
				print("rate = " + index)


def get_beacon(*args,  **kwargs):
	"""
	Function For Filtering Beacon Frames And Extract Access 
	Point Information From Captured Packets.
	"""

	# create monitor interface using iw
	cmd = '/sbin/iw dev %s interface add %s type monitor >/dev/null 2>&1' \
		% ("wlp3s0", "mon0")
	try:
		os.system(cmd)
	except:
		raise
	
	scapy.sniff(prn=PacketHandler, *args, **kwargs)
	return (ap, packets)


if __name__=="__main__":

	get_beacon(iface="mon0", timeout=10)


# int(binascii.hexlify('\x83'), 16)
