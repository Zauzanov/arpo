from multiprocessing import Process
from scapy.all import (ARP, Ether, conf, get_if_hwaddr,
                       send, sniff, sndrcv, srp, wrpcap)
import os
import sys
import time 

def get_mac(targetip):                                                      # Defines a func to get the speficied PC's MAC-address.
    pass

class Arpo:
    def __init__(self, victim, gateway, interface='eth0'):
        pass

    def run(self):
        pass

    def poison(self):                                                       # To replace network parameters.
        pass

    def sniff(self, count=200):                                             # To extract network parameters.
        pass

    def restore(self):                                                      # To restore network parameters.
        pass

if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    myarp = Arpo(victim, gateway, interface)
    myarp.run()