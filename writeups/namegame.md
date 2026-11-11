### NAME - GAME CTF ### -Skill bit
 
 we start by getting the pcap file

![scan](/writeups/images/file.png)


Overview

A single packet capture: capture.pcap. A suspicious workstation was generating unusual DNS traffic, and we need to figure out what was exfiltrated.

***Reconnaissance***

We can see the below pcap file image

![recon](/writeups/images/gname1.png)

Open capture.pcap in Wireshark. At first glance it looks like a normal pcap of random DNS queries for Google, GitHub, Discord, etc. But scrolling through the DNS queries, one domain stands out immediately:
```bash
4d657461.totallynotac2.meatctf.com
4354467b.totallynotac2.meatctf.com
646e735f.totallynotac2.meatctf.com
```

![meta](/writeups/images/gname2.png)

The base domain totallynotac2.meatctf.com is obviously suspicious. The subdomain prefixes — 4d657461, 4354467b, 646e735f — all look like hex strings.

***What is this?***

This is DNS exfiltration: a classic data exfiltration technique where an attacker encodes stolen data into DNS subdomain queries. Since DNS is almost never blocked or inspected (firewalls let it through, IDS rarely flags it), it's a stealthy channel for smuggling data out of a network.

The attacker's tool on the compromised machine:

    Hex-encoded the stolen data
    Split it into 8-character chunks
    Sent one DNS query per chunk, using each chunk as a subdomain prefix
    Their C2 server logged the incoming queries and reassembled the data


***Recovering the data***

We can view what was in the hex with a simple bash one-liner using tshark:

we can use the tshark command as below:

```bash
tshark -r capture.pcap \
  -Y 'dns.qry.name contains "totallynotac2"' \
  -T fields -e dns.qry.name \
  | sed 's/\.totallynotac2.*//' \
  | tr -d '\n' \
  | xxd -r -p
```

| Code | Explanation |
| --- | --- |
| `tshark -r capture.pcap` | Reads the packet capture. |
| `-Y 'dns.qry.name contains "totallynotac2"'` | Applies a Wireshark display filter. |
| `-T fields -e dns.qry.name` | Outputs selected fields and prints the queried domain names. |
| `sed 's/\.totallynotac2.*//'` | Strips the domain suffix. |
| `tr -d '\n'` | Removes newlines to join the hex. |
| `xxd -r -p` | Converts hex back to data. |


![flag](/writeups/images/gname3.png)

Glad you enjoyed it.