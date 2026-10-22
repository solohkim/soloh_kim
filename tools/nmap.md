### Introduction

When it comes to mapping a network, one name always comes up: Nmap. A must-have in the world of cybersecurity, this Swiss army knife of network reconnaissance is the tool of choice for identifying exposed services, detecting open ports and laying the foundations for an effective internal penetration test.

As infrastructures become increasingly hybrid and complex, the ability to accurately visualise accessible systems is more crucial than ever. In this respect, Nmap remains the industry standard.

Thanks to its multiple features, it can not only scan hosts, but also detect software versions, identify operating systems and observe the reactions of firewalls or IDS in place.

In this article, we will illustrate the principle of network reconnaissance (mapping and discovery) through a detailed presentation of Nmap’s operation and features, supported by case studies.

What is Nmap?
Nmap, short for Network Mapper, is a key open source tool in the world of cybersecurity. Available as a command-line application and via a graphical interface (Zenmap), it runs on most operating systems.

Nmap is generally used to collect network information on any type of device with an IP address, whether it’s an isolated machine or a set of hosts on an entire network. Nmap was originally designed for two basic purposes:

Scan a specific host to identify active services and open ports;
Scan a network to detect connected hosts.
Over the years, its functionality has expanded considerably. Thanks to its many modules, Nmap is now a veritable Swiss Army Knife of network reconnaissance.

What’s more, Nmap is a versatile tool, equally suited to personal and professional use. Free and accessible, it enables anyone to identify the active services on a system. But it is above all in a professional context that it really comes into its own: whether it’s to make an inventory of the hosts and services on a network or to detect risky configurations.

When it comes to cyber security, identifying exposed services, which may be vulnerable or poorly configured, is a key step in assessing a network’s level of security. And this is precisely what Nmap can do.

Nmap usage example
Before going into detail, let’s illustrate how Nmap works with a concrete example: scanning a host having an IP address of 172.20.0.2.


![scan](/tools/images/nmap1.png)


Nmap tells us that port 80 is open and that an HTTP service is probably active there. It also indicates that 999 other ports are closed.

Note that, by default, Nmap only scans the 1,000 most commonly used ports; this behaviour can be changed using the -p option.

In the following sections, we’ll take a closer look at how Nmap works and how it achieves these results. We’ll detail the different stages of a typical run, the scanning techniques available, and key features such as version detection and operating system identification.

Finally, we will look at the more advanced uses of Nmap, adapted to specific contexts such as firewall evasion or automation via scripts.

Each Nmap run follows a structured sequence of steps. Depending on the options specified, some may be skipped, while others are only executed when explicitly requested.

The table below summarises these different phases, in the order in which they are usually executed:

| No. | Phase | Description |
| --- | --- | --- |
| 1 | **Pre-scan with scripts** | Executes scripts from the `prerule` category, before any scanning phase. These may send broadcast or DNS queries, for example. *Default: no - Option: --script or -sC* |
| 2 | **Target enumeration** | Generates the list of IPs to scan. Domain names are resolved during this phase. *Default: yes - Option: cannot be disabled* |
| 3 | **Host discovery** | Detects whether each host is up or not. *Default: yes - Option: can be disabled with -Pn* |
| 4 | **Reverse DNS resolution** | Attempts to retrieve domain names associated with IP addresses. *Default: yes - Option: can be disabled with -n* |
| 5 | **Port scanning** | Nmap's core function: identifying the state of ports using different techniques. *Default: yes - Option: can be disabled with -sn* |
| 6 | **Version detection** | Identifies the services and versions running on... |

Phases of an Nmap execution
In the following sections, we’ll focus on phases 3 (host discovery), 5 (port scanning), 6 (version detection) and 7 (OS detection), which are particularly interesting for understanding the power of Nmap.

Port scanning and scanning techniques
This phase corresponds to the fifth stage shown in the table above. The aim here is to identify which ports are open on a host.

However, with the spread of security solutions at various levels – such as firewalls that block certain connections according to predefined rules – it is becoming difficult to know whether a port is actually listening or not.

This is why Nmap classifies the status of a port into several categories:

Open
Closed
Filtered
Unfiltered: in some cases, Nmap cannot determine whether the port is open or closed, but it can tell whether it is filtered or not from the responses it receives.
Nmap offers many scanning techniques that can be used to deduce the status of a port by exploiting subtle differences in protocol implementations between devices and operating systems.

These methods are not always reliable, since they depend on the specific behaviour of targets, but they are still useful to know, especially when interacting with atypical systems or devices. Some of them have also been designed to be discreet.

Let’s take a look at some of the port scanning techniques offered by Nmap.

TCP SYN Scan (-sS)
This technique requires raw packet privileges and is used by default if the user running Nmap has the necessary rights. It works with any TCP-compliant service.

The principle is as follows: Nmap sends a packet to the target port with only the SYN flag set.

If a SYN/ACK (or sometimes just SYN) response is received, this means that the port is open.
If an RST (reset) response is received, the port is closed.
In the event of no response or if an ICMP ‘Destination unreachable’ message is received, the port is considered to be filtered.
The TCP SYN scan is often referred to as a stealth scan, because Nmap does not establish a full connection: it sends an RST packet immediately after receiving a SYN/ACK, interrupting the handshake procedure before it is finalised.

TCP Connect Scan (-sT)
This technique is selected by default if the user running Nmap does not have the necessary privileges to send raw packets.

It is based on the classic establishment of a full TCP connection with the target port, following the standard TCP handshake process. It detects port states in the same way as the SYN scan, with one difference: the TCP connect scan is not stealthy.

This method completes the TCP connection by responding with a SYN/ACK, making it easy to detect. Most modern systems log all connection attempts, which can attract the attention of security solutions or network administrators.

TCP ACK Scan (-sA)
Unlike previous techniques which exploit only the SYN flag, this method sends a packet with only the ACK flag set.

When an open or closed port receives a packet containing only this ACK flag, it should respond with a packet containing an RST flag. So if Nmap receives an RST in response, the port is classified as unfiltered. On the other hand, if there is no response or if it receives an ICMP ‘destination unreachable’ message, the port is filtered.

It is therefore important to note that this technique does not indicate whether a port is open or closed, but only whether or not it is accessible through a firewall.

This approach can nevertheless be useful for analysing the configuration of a firewall. For example, it can sometimes be used to distinguish whether a firewall is stateless or stateful. Stateful firewalls keep a record of established connections and generally only allow packets belonging to an active session, or those attempting to initiate a new one.

Despite its limitations, the TCP ACK scan can be used in conjunction with other techniques. By cross-checking the results, it is possible to infer whether a port is open or closed.

UDP Scan (-sU)
UDP scanning consists of sending empty UDP packets to the target ports, then waiting for any response. If the port responds with data, it is considered open.

However, it should be borne in mind that UDP services rarely respond to empty packets or unexpected data. This makes it difficult for Nmap to know whether the lack of response is due to a service ignoring the packet, or a firewall blocking the traffic.

To increase the chances of getting a response, Nmap sometimes sends data specific to certain protocols to known ports. For example, it sends a DNS request to port 53.

When no response is received, Nmap classifies the status of the port as ‘open|filtered’, as it is unable to make a decision.

Finally, it should be noted that UDP scanning is relatively slow, as Nmap waits several seconds by default before retransmitting a packet.

TCP NULL Scan (-sN)
So far, we’ve seen techniques that exploit the SYN and ACK flags. This method, on the other hand, sends a TCP packet without any flags set – hence the name NULL scan.

It is based on a specific detail in the TCP RFC, which stipulates that when a closed port receives a packet without the RST flag set, it must respond with an RST packet.

Thus, by sending a packet that does not contain any of the RST, SYN or ACK flags, it becomes possible to identify closed ports on systems that apply this RFC-compliant behaviour.

However, this technique has one limitation: it cannot distinguish between an open port and a filtered port. The RFC states that an open port should simply ignore packets that do not contain flags SYN, ACK or RST.

TCP FIN Scan (-sF)
This technique works in the same way as the TCP NULL scan, except that it sends packets with the FIN flag set.

TCP Xmas Scan (-sX)
This technique is similar to the previous one, except that the packets sent have the FIN, PSH and URG flags set, giving them a ‘Christmas tree’ appearance (hence the name Xmas).

TCP Window Scan (-sW)
This technique is similar to the TCP ACK scan in that it sends packets with only the ACK flag set, but it interprets the responses differently.

It attempts to exploit a behaviour present on some systems: they respond with an RST packet whose window field varies according to the state of the port.

If the port is open, the window field contains a non-zero value.
If the port is closed, this value is generally zero.
This technique only works on systems that implement this specific behaviour, which makes it unreliable overall.

SCTP INIT Scan (-sY)
The SCTP protocol is an alternative to the TCP/UDP protocols. Similar to the SYN scan, this technique detects that a port is open if it receives an INIT-ACK packet in response.

Conversely, if it receives an ABORT packet, it considers the port to be closed.

Finally, if an ICMP ‘destination unreachable’ error is received, the port is classified as filtered.

Custom scans with --scanflags
Nmap is a flexible tool that allows users to create custom scans by specifying any combination of TCP flags.

It is also possible to add a scan option such as -sF or -sA so that the results are interpreted according to the behaviour of that type of scan.

If no option is specified, the results are interpreted by default as a SYN (-sS) scan.

Scan techniques summary
TCP
The table below summarises how the various TCP scanning techniques described above classify ports according to the responses they receive.

![scan](/tools/images/nmap2.png)

UDP
The table below summarises the cases encountered when using the UDP scan technique.


![scan](/tools/images/nmap3.png)

Detecting services and versions with Nmap
This corresponds to the sixth phase mentioned in the table showing Nmap’s execution phases.

At this stage, all the examples we have seen include a SERVICE column in the output, indicating values such as http.

This is because, by default, Nmap tries to guess which service is running on a given port based on a file called nmap-services. This file associates port numbers with the services that are usually linked to them.

However, this method is imprecise, as users are free to run any program on any port, without necessarily respecting the conventions.

In the example below, Nmap correctly identifies that an http service is running on port 80. This information appears in the nmap-services file (since port 80 is a registered port, commonly used for HTTP servers).

However, it is unable to identify exactly what is running on port 5000, and simply describes it as upnp. This is logical because port 5000 is not an officially registered port, so it does not appear in the nmap-services file


![scan](/tools/images/nmap4.png)

To get around this limitation and gather as much information as possible about targets, Nmap offers a complete module dedicated to service detection. This module is based on a fingerprinting method, which is much more effective than the approach based solely on the nmap-services static file.

This module can be activated by adding the -sV option. Rerunning the previous scan with this option gives the following results:

![scan](/tools/images/nmap5.png)

The results now display a new VERSION column, which indicates that the service listening on port 5000 is most likely a nginx HTTP server, version 1.27.4.

If this version of nginx is vulnerable, this information could be extremely valuable to an attacker. This is why the type of service and its version are crucial information from a security point of view.


### How does service detection work in Nmap?


During a scan, Nmap doesn’t just list open ports. It can also try to identify the services running on these ports. To do this, it uses a file called nmap-service-probes, which contains a large list of ‘probes’.

A probe is simply a small, specific message that Nmap sends to a port to see how the service will respond. By comparing the response it gets with what it expects, Nmap can guess which service is up against it (for example Apache, nginx, SSH, etc.).

These probes can be modified or enhanced by advanced users to detect specific services.

Below is an example of a probe:

![scan](/tools/images/nmap6.png)

Each probe contains several lines of directives:

The Probe line describes the protocol used (TCP or UDP), the name of the probe, and the content of the message sent to the port (the ‘payload’).
The match lines contain regular expressions: they are used to check whether the service response matches a known pattern. If it matches, the service is identified!
The ports directive lists the ports on which this probe is usually effective.
Detection process stages
For each port found to be open or open|filtered, Nmap proceeds as follows:

It selects the compatible probes (protocol + port mentioned).
It sends each probe to the port :
If a response is received, it tests the response with the match rules. When none matches, it tries a fallback probe.
If no response is received, it moves on to the next probe.
If no probe matches :
Nmap tries some other probes, even if the port is not specifically mentioned.
It then takes into account the rarity of the probe (rarity) and the level of verbosity requested (--version-intensity).
However, it is important to note that the results of this phase are not always 100% reliable, as they depend on a database and regular expression matching tests. Detection errors can occur.

For this reason, Nmap encourages users to report errors or contribute to the probes database.

Case of UDP services
As mentioned in previous sections, open UDP ports are prone to timeouts, as many UDP services will not respond if they do not recognise the data received.

In contrast, the service detection phase sends protocol-specific data, which increases the chances of sending the expected data to the UDP service and getting a response back.

In this case, any UDP port previously marked as open|filtered can be updated to open.

How to detect the operating system in this phase?
The service detection phase can also identify operating systems, as many services can reveal useful information simply by interacting with them.

For example, SSH often sends a banner that may contain details of the server’s operating system. It is therefore possible to extract information about the OS during this phase.

In addition, some services are known to run exclusively on specific systems or devices, allowing Nmap to infer the underlying operating system.

However, Nmap provides another mechanism for operating system detection that is invoked using the -O option, which will be detailed in another section.

Focus on ports excluded by default in the service detection phase
As a precaution, by default Nmap ignores ports 9100 to 9107, which are often associated with printers. Printers, as mentioned in the documentation, have a bad habit of printing everything you send them.

So if an HTTP server is running on one of these ports, it will not be detected by default. Example:


We see that the port has not been identified as an HTTP server. But if we add --allports to force Nmap to scan all ports:


Nmap can identify the service and version.

Nmap host discovery
In addition to port scanning, Nmap can also detect the hosts accessible on a given network. This feature is particularly useful for system or network administrators, as it facilitates infrastructure management and the creation of a network inventory.

Several techniques are available for this purpose.

Using the ICMP protocol
ICMP Echo Request (-PE): Nmap sends an ICMP Echo request and waits for a response (Echo Reply). If no response is received, the machine is considered to be offline. This is the default ping behaviour.
ICMP Address Mask Request (-PM): Works like -PE, but sends an ICMP Address Mask request. Useful if Echo requests are blocked.
ICMP Timestamp Request (-PP): Sends an ICMP Timestamp request to determine whether the host responds.
Using the ARP protocol (-PR)
This method is particularly effective on local networks. As the ARP protocol is widely used and rarely blocked, it is a reliable solution for detecting active machines on a LAN.

Using TCP/UDP protocols
-PS: Sends a TCP SYN packet to port 443 (configurable). If a SYN/ACK or RST response is received, the host is considered active. This works well when ICMP is blocked, but services such as HTTP are allowed.
-PA: Same logic as -PS, but sends a TCP ACK packet on default port 80.
-PU: Sends a UDP packet, by default on port 40125.
Use of other IP protocols (-PO)
Nmap can also attempt to detect the presence of a host via other protocols, such as IGMP.

By default, Nmap combines the following options:

For privileged users: PE -PP -PS443 -PA80
For non-privileged users: PS80,443
Below is an example of scanning a machine on a network

![scan](/tools/images/nmap7.png)


#### Advanced usage of Nmap
## OS detection
Identifying the operating system used by a target is valuable information. For example, it can be used to identify the type of device, such as routers or printers, which often run specific systems.

In a security audit, this data is crucial for adapting attack payloads to the targeted environment.

Nmap includes a dedicated operating system detection module, based on network fingerprinting. This method relies on a series of metrics and calculations to compare the characteristics of an unknown host with a database of known references.

However, this detection may fail or produce inaccurate results. In such cases, Nmap provides a list of likely operating systems, accompanied by a trust percentage. It may also happen that the system cannot be identified at all.

How does OS detection work in Nmap?
The following explanations apply exclusively to IPv4.

Operating system detection relies on sending several types of probes to the target. These packets may be TCP, UDP or ICMP in nature, and often include unusual data in certain fields of the packet. Nmap sends around 16 different packets and classifies the results into a dozen categories.

After receiving the responses, Nmap builds a subject fingerprint by assigning specific attributes to each category, based on the returned values or calculated metrics. This fingerprint is then compared with a reference fingerprint extracted from Nmap’s database of known signatures for numerous operating systems.

Here’s an example of OS detection performed on a router, using the -d option to display details of the calculated fingerprint:

```bash
# nmap -O -d -sV 192.168.1.254

Not shown: 992 closed tcp ports (reset)
PORT     STATE SERVICE  REASON         VERSION
53/tcp   open  domain   syn-ack ttl 64 dnsmasq 2.90
[... TRUNCATED RESULTS ...]

Device type: general purpose|router

Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, OpenWrt 21.02 (Linux 5.4), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
TCP/IP fingerprint:
OS:SCAN(V=7.95%E=4%D=5/1%OT=53%CT=1%CU=42846%PV=Y%DS=1%DC=D%G=Y%M=8C97EA%TM
OS:=68133D2C%P=arm-apple-darwin24.1.0)SEQ(SP=104%GCD=1%ISR=10D%TI=Z%CI=Z%II
OS:=I%TS=A)OPS(O1=M5B4ST11NW7%O2=M5B4ST11NW7%O3=M5B4NNT11NW7%O4=M5B4ST11NW7
```
The TCP/IP fingerprint block (not shown here in full) illustrates the wealth of data collected by Nmap. From this data, Nmap identified three possible operating systems for the target:

Linux 4.15 to 5.19
OpenWrt 21.02 (Linux kernel 5.4)
MikroTik RouterOS 7.2 to 7.5 (Linux kernel 5.6.3)
In addition, Nmap indicates that the targeted equipment is probably a router or standard machine.
