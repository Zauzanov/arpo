# arpo
<p align="center">
  <h1 align="center"> an educational/research Scapy-based ARP-spoofing tool </h1>
	<p align="center">For cybersecurity professionals and educational purposes only!</p>
	<p align="center">Use only on hosts/networks you own or have permission to test!</p>
</p>

## 0. Check our MAC and IP addresses on our Kali machine:
```bash
ifconfig eth0
eth0: 	flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
    	inet 192.168.204.139  netmask 255.255.255.0  broadcast 192.168.204.255 			# Kali IP-address!
        inet6 fe80::b6f5:2d19:3b92:87e7  prefixlen 64  scopeid 0x20<link> 				 
        ether 00:0c:29:47:74:ba  txqueuelen 1000  (Ethernet) 							# Kali MAC-address!

```
Let's highlight them - Kali addresses: 
- IP: **192.168.204.139** 
- MAC: **00:0c:29:47:74:ba**

## 1. Check the ARP-cache on the victim machine(Metasploitable2 - an intentionally vulnerable VM):
```bash
arp -a
```
### Its ARP-cache before the attack:
![meta2_before](https://)

### On MacOS it can look like this: 
```bash
kali.attlocal.net (192.168.1.203) at a4:5e:60:ee:17:5d on en0 ifscope 				# Our kali machine
dsldevice.attlocal.net (192.168.1.254) at 20:e5:64:c0:76:d0 on en0 ifscope 			# Attacker and target share the same network and connect to the internet using the same gateway(192.168.1.254) with this MAC-address: 20:e5:64:c0:76:d0
? (192.168.1.255) at ff:ff:ff:ff:ff:ff on en0 ifscope [ethernet]
```
These values are going to be useful, as we will be able to see ARP-cache during the attack and see how the gateway's registered MAC-address are going to be changed.

Knowing gateway's and target's adresses, we can proceed. 

## 0. Here we see that the attacker and the victim share the same gateway:

### Kali machine before: 
![kali_before](https://raw.githubusercontent.com/Zauzanov/)


## 2. Secondly, we need to inform the local system(Kali) that we are going to send packets to IP addresses belonging to both the gateway and the victim computer:

### For Linux(Kali):
```bash
echo 1 > /proc/sys/net/ipv4/ip_forward
# or
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
```

### For macOS:
```bash
sudo sysctl -w net.inet.ip.forwarding=1 
```
## 3. So, after configuring IP address forwarding, let's run our script(on Kali) and check the ARP cache of the victim computer:

```bash
python arpo.py [VICTIM_IP] [GATEWAY_IP] [NIC]
python arpo.py 192.168.204.129 192.168.204.2 eth0 			# An Instance. 
```

## 4. While the script is capturing 100 packets, let's output content of the ARP-table on the victim machine:
```bash
arp -a  
```
If success, these MAC-addresses have to have the same values, like this: 
#### OUTPUT:
```bash
kali.attlocal.net (192.168.1.203) at a4:5e:60:ee:17:5d on en0 ifscope 				# Our kali machine
dsldevice.attlocal.net (192.168.1.254) at a4:5e:60:ee:17:5d on en0 ifscope          # The gateway
```

We're good, if the gateway has the same MAC-address as the attacker machine does. 