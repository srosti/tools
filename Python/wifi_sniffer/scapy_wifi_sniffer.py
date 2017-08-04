from scapy.all import *
ap_list = []
def BeaconFrameHandler(pkt):
    print("Got network packet")
    if pkt.haslayer(Dot11):
        print("Got 802.11 packet")
        if pkt.type == 0 and pkt.subtype == 8:
            if pkt.addr2 not in ap_list:
                ap_list.append(pkt.addr2)
                print("Found bssid={} with SSID={}".format(pkt.addr2, pkt.info))

sniff(iface = "wlx00026f855193", prn = BeaconFrameHandler)
sniff(iface = "wlp3s0", prn = BeaconFrameHandler)
