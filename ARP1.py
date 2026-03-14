from scapy.all import *
from scapy.layers.l2 import Ether, ARP
conf.iface = "Intel(R) Dual Band Wireless-AC 3165"
pkt = Ether(dst="D8:9B:3B:1E:2D:89")/ARP(pdst="192.168.43.252")
result = srp1(pkt, timeout=2, verbose=False)
print(result)