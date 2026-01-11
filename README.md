# arpo
<p align="center">
  <h1 align="center"> an educational/research Scapy-based ARP-spoofing tool </h1>
	<p align="center">For cybersecurity professionals and educational purposes only!</p>
	<p align="center">Use only on hosts/networks you own or have permission to test!</p>
</p>

## Check the ARP-cache on the victim machine:
```bash
arp -a
```

### On MacOS it can look like this: 
```bash
kali.attlocal.net (192.168.1.203) at a4:5e:60:ee:17:5d on en0 ifscope 				# Our kali machine
dsldevice.attlocal.net (192.168.1.254) at 20:e5:64:c0:76:d0 on en0 ifscope 			# Attacker and target share the same network and connect to the internet using the same gateway(192.168.1.254) with this MAC-address: 20:e5:64:c0:76:d0
? (192.168.1.255) at ff:ff:ff:ff:ff:ff on en0 ifscope [ethernet]
```
These values are going to be useful, as we will be able to see ARP-cache during the attack and see how the gateway's registered MAC-address are going to be changed.

Knowing gateway's and target's adresses, we can proceed.

## On Mac: If success, these MAC-addresses have to have the same values, like this: 
#### MacOS OUTPUT:
```bash
kali.attlocal.net (192.168.1.203) at a4:5e:60:ee:17:5d on en0 ifscope 				# Our kali machine
dsldevice.attlocal.net (192.168.1.254) at a4:5e:60:ee:17:5d on en0 ifscope          # The gateway
```
We're good, if the gateway has the same MAC-address as the attacker machine does. 