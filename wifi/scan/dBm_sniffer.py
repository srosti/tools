import threading, os, time, random
from scapy.all import *

def hopper(iface):
    n = 1
    stop_hopper = False
    while not stop_hopper:
        time.sleep(0.50)
        os.system('iwconfig %s channel %d' % (iface, n))
        dig = int(random.random() * 14)
        if dig != 0 and dig != n:
            n = dig

F_bssids = []    # Found BSSIDs
def findSSID(pkt):
    if pkt.haslayer(Dot11Beacon):
       if pkt.getlayer(Dot11).addr2 not in F_bssids:
           F_bssids.append(pkt.getlayer(Dot11).addr2)
           ssid = pkt.getlayer(Dot11Elt).info
           dBm = pkt.dBm_AntSignal
           print("ssid=%s dBm=%d" % (ssid, dBm))

if __name__ == "__main__":
#    interface = "wlan1mon"
    interface = "mon0"
#    thread = threading.Thread(target=hopper, args=(interface, ), name="hopper")
#    thread.daemon = True
#    thread.start()

    sniff(iface=interface, prn=findSSID)
