from scapy.all import all
ap_list = []
def BeaconFrameHandler(pkt):
    if pkt.haslayer(Dot11):
        if pkt.type == 0 and pkt.subtype == 8:
            if pkt.addr2 not in ap_list:
                ap_list.append(pkt.addr2)
                print("Found bssid={} with SSID={}".format(pkt.addr2, pkt.info))

sniff(iface="en0", prn = BeaconFrameHandler)