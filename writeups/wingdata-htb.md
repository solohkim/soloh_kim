HackThBox WingData Writeup

INTRO
A walkthrough of the HackTheBox ‘WingData’ machine. This write-up covers initial access, privilege escalation, and post-exploitation techniques.

Key Highlights
Ready to take on the WingData machine on Hack The Box? This guide provides a complete walkthrough for your penetration testing journey. While there’s no universal exploit script dedicated solely to WingData, the walkthrough will help you identify and craft custom scripts or modify public exploits as needed depending on the vulnerabilities you uncover. Here’s a glimpse of what you’ll learn:

### Ping IP
Before we start scanning we'll ping our machine on the network to see if it's reachable via the VPN.

![ping check - WingData](writeups/images/ping.png)

### Initial NMAP Scanning
We'll perform a basic nmap scan to see the services, open ports and other scripts on the machine.

We'll use commands for TCP full scan:

```bash
nmap -sC -sV -p- -T4 10.129.x.x


