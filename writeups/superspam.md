Initial Access

nmap -sC -sV -p- -A -T4 superspam.thm

\-sC → Runs the default NSE scripts (like ftp-anon, http-title, vnc-info, etc.)

\-sV → Detects service versions (e.g., Apache 2.4.29, OpenSSH 7.6p1)

\-p- → Scans all 65,535 TCP ports

\-A → Aggressive scan: combines OS detection, version detection, script scanning, and traceroute

\-T4 → Speeds up the scan (aggressive timing)

PORT     STATE SERVICE VERSION

80/tcp   open  http    Apache httpd 2.4.41 ((Ubuntu))

|\_http-title: Home :: Super-Spam

|\_http-server-header: Apache/2.4.41 (Ubuntu)

|\_http-generator: concrete5 - 8.5.2

4012/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.13 (Ubuntu Linux; protocol 2.0)

| ssh-hostkey: 

|   3072 54:4c:d3:a1:55:f6:7d:cf:fd:22:f4:d1:30:66:2a:8b (RSA)

|   256 1c:43:31:4c:50:fb:70:79:87:bd:5f:e9:a2:5e:6b:fd (ECDSA)

|\_  256 70:37:63:b0:2e:53:6d:5a:e4:d4:e9:f7:6a:b2:d9:af (ED25519)

4019/tcp open  ftp     vsftpd 3.0.5

| ftp-anon: Anonymous FTP login allowed (FTP code 230)

| drwxr-xr-x    2 ftp      ftp          4096 Feb 20  2021 IDS\_logs

|\_-rw-r--r--    1 ftp      ftp           526 Feb 20  2021 note.txt

| ftp-syst: 

|   STAT: 

| FTP server status:

|      Connected to ::ffff:192.168.192.205

|      Logged in as ftp

|      TYPE: ASCII

|      No session bandwidth limit

|      Session timeout in seconds is 300

|      Control connection is plain text

|      Data connections will be plain text

|      At session startup, client count was 2

|      vsFTPd 3.0.5 - secure, fast, stable

|\_End of status

5901/tcp open  vnc     VNC (protocol 3.8)

| vnc-info: 

|   Protocol version: 3.8

|   Security types: 

|     VNC Authentication (2)

|     Tight (16)

|   Tight auth subtypes: 

|\_    STDV VNCAUTH\_ (2)

6001/tcp open  X11     (access denied)

No exact OS matches for host (If you know what OS is running on it, see https://nmap.org/submit/ ).

TCP/IP fingerprint:

OS:SCAN(V=7.95%E=4%D=10/17%OT=80%CT=1%CU=38922%PV=Y%DS=3%DC=T%G=Y%TM=6AD389

OS:1D%P=x86\_64-pc-linux-gnu)SEQ(SP=104%GCD=1%ISR=10C%TI=Z%CI=Z%II=I%TS=A)SE

OS:Q(SP=105%GCD=1%ISR=10C%TI=Z%CI=Z%II=I%TS=A)SEQ(SP=106%GCD=1%ISR=107%TI=Z

OS:%CI=Z%II=I%TS=A)SEQ(SP=106%GCD=1%ISR=10A%TI=Z%CI=Z%II=I%TS=A)SEQ(SP=FE%G

OS:CD=1%ISR=102%TI=Z%CI=Z%II=I%TS=A)OPS(O1=M4E6ST11NW7%O2=M4E6ST11NW7%O3=M4

OS:E6NNT11NW7%O4=M4E6ST11NW7%O5=M4E6ST11NW7%O6=M4E6ST11)WIN(W1=F4B3%W2=F4B3

OS:%W3=F4B3%W4=F4B3%W5=F4B3%W6=F4B3)ECN(R=Y%DF=Y%T=40%W=F507%O=M4E6NNSNW7%C

OS:C=Y%Q=)T1(R=Y%DF=Y%T=40%S=O%A=S+%F=AS%RD=0%Q=)T2(R=N)T3(R=N)T4(R=Y%DF=Y%

OS:T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T5(R=Y%DF=Y%T=40%W=0%S=Z%A=S+%F=AR%O=%RD

OS:=0%Q=)T6(R=Y%DF=Y%T=40%W=0%S=A%A=Z%F=R%O=%RD=0%Q=)T7(R=Y%DF=Y%T=40%W=0%S

OS:=Z%A=S+%F=AR%O=%RD=0%Q=)U1(R=Y%DF=N%T=40%IPL=164%UN=0%RIPL=G%RID=G%RIPCK

OS:=G%RUCK=G%RUD=G)IE(R=Y%DFI=N%T=40%CD=S)

What CMS and version is being used?



concrete5 8.5.2

FTP

ftp superspam.thm 4019

Press enter or click to view image in full size



We found note.txt and 3 pcap files in IDS\_logs Directory



12-01-21.req.pcapng  13-01-21.pcap  14-01-21.pcapng 

Press enter or click to view image in full size



This reads like a timeline of escalating incidents: Adam notices strange IDS alerts, collects packet captures with Wireshark, then finds his blog mysteriously deleted. Finally, Super‑spam reveals himself with a mocking note. It’s essentially a breadcrumb trail showing how the attacker gradually made their presence felt.



NTLMv2 Password Cracking

14–01.-21.pcap — this file had the sessions login details inside (NTLMv2)



1.Copy Domain Name and User name to a text file



Press enter or click to view image in full size



ntlmssp

2\. NTLM Secure Service Provider >> NTLM Response section >> NTProofStr and NTLMv2 response, copy both of these as hex stream



Press enter or click to view image in full size



3\. filter ntlmssp.ntlmserverchallenge Copy this value to the text document as a Hex stream



Press enter or click to view image in full size



Domain name: 3B

User name: lgreen

ServerChallange: a2cce5d65c5fc02f

NTProofStr: 73aeb418ae0e8a9ec167c4d0880cfe22

NTLMv2 Response: 73aeb418ae0e8a9ec167c4d0880cfe22

010100000000000049143c43a261d6012ce41adf31a1363c00000000020004003300420001001e003000310035003600360053002d00570049004e00310036002d004900520004001e0074006800720065006500620065006500730063006f002e0063006f006d0003003e003000310035003600360073002d00770069006e00310036002d00690072002e0074006800720065006500620065006500730063006f002e0063006f006d0005001e0074006800720065006500620065006500730063006f002e0063006f006d000700080049143c43a261d60106000400020000000800300030000000000000000100000000200000fc849ef6b042cb4e368a3cbbd2362b5ccc39324c75df3415b6166d7489ad1d2b0a001000000000000000000000000000000000000900220063006900660073002f003100370032002e00310036002e00360036002e0033003600000000000000000000000000

Use This Fomat and Save as hash.txt



User name::Domain name:ServerChallange:NTproofstring:(modified)NTLMv2 Response

Then we got



lgreen::3B:a2cce5d65c5fc02f:73aeb418ae0e8a9ec167c4d0880cfe22:010100000000000049143c43a261d6012ce41adf31a1363c00000000020004003300420001001e003000310035003600360053002d00570049004e00310036002d004900520004001e0074006800720065006500620065006500730063006f002e0063006f006d0003003e003000310035003600360073002d00770069006e00310036002d00690072002e0074006800720065006500620065006500730063006f002e0063006f006d0005001e0074006800720065006500620065006500730063006f002e0063006f006d000700080049143c43a261d60106000400020000000800300030000000000000000100000000200000fc849ef6b042cb4e368a3cbbd2362b5ccc39324c75df3415b6166d7489ad1d2b0a001000000000000000000000000000000000000900220063006900660073002f003100370032002e00310036002e00360036002e0033003600000000000000000000000000

Press enter or click to view image in full size



P@$$w0rd

Wifi Password Cracking

Login FTP as Anonymous then Download 2 files .quicknote.txt and SamsNetwork.cap in .cap directory.



ftp superspam.thm 4019

Press enter or click to view image in full size



Press enter or click to view image in full size



Super‑spam is leaving taunting “souvenirs” in the form of .cap (packet capture) files — essentially bragging that he recorded how he broke in. In security terms, a .cap file is a Wireshark/tcpdump capture that can contain authentication attempts, suspicious traffic, or exploit traces.



Write on Medium

What this message tells us in the incident storyline:



He’s confident his intrusion worked.

He deliberately left behind evidence (the .cap file) as a trophy.

He’s mocking defenders by declaring his “Linux‑free galaxy” plan and praising Windows.

Use aircrack-ng crack password



aircrack-ng SamsNetwork.cap -w /usr/share/wordlists/rockyou.txt

Press enter or click to view image in full size



sandiago

RCE(www-data)

we found against all 4 blog users we located and one of them logs us in



Press enter or click to view image in full size



http://superspam.thm/concrete5/index.php/blog

User found



Benjamin\_Blogger

Lucy\_Loser

Adam\_Admin

Donald\_Dump

lgreen

1.Login as Donald\_Dump



Donald\_Dump:sandiago

Press enter or click to view image in full size



http://superspam.thm/concrete5/index.php/login

2\. Click Dashboard and select System \& Settings >> Files >> Allowed File Types then add php to textbox and Save



Press enter or click to view image in full size



http://superspam.thm/concrete5/index.php/dashboard/system/files/filetypes

4\. I am testing/analyzing webshells or reverse shells, specifically using c99shell.



Press enter or click to view image in full size



5\. Download d.png



Press enter or click to view image in full size



you can just see the password without needing to reverse the xor routine.



Press enter or click to view image in full size



$$L3qwert30kcool

What is the user flag?



flag{-eteKc=skineogyls45«ey?t+du8}

Press enter or click to view image in full size



What type of encryption did super-spam use to send his encrypted messages?



XOR

What key information was embedded in one of super-spam’s encrypted messages?



$$L3qwert30kcool

VNC(Root)

1.Download passswd file and vnc password decrypter



scp -P 4012 donalddump@superspam.thm:/home/donalddump/passwd ./passwd

Press enter or click to view image in full size



git clone https://github.com/jeroennijhof/vncpwd.git

Press enter or click to view image in full size



2\. Complie .c program



gcc -o vncpwd vncpwd.c d3des.c

The code in d3des.c uses old-style function definitions (pre-ANSI C). Although it generates a lot of warnings, the vncpwd binary was successfully built—so you can run it directly. These warnings won't affect performance in the lab, as this code is specifically intended for decoding VNC passwords.



Press enter or click to view image in full size



3\. Run vnc password decrypter



Press enter or click to view image in full size



vncpriv

4\. Connect to a VNC server.



vncviewer -passwd passwd superspam.thm:5901

vncviewer → the client program to connect to a VNC server.

\-passwd passwd → tells the viewer to use the password stored in the file called passwd. This file must be in the format that VNC expects (binary, not plain text). Tools like vncpwd can generate or decode this file.

superspam.thm:5901 → the target host (superspam.thm) and port (5901) where the VNC service is running.

Press enter or click to view image in full size



Press enter or click to view image in full size



MZWGCZ33NF2GKZKLMRRHKPJ5NBVEWNWCU5MXKVLVG4WTMTS7PU======



KRUGS4ZANFZSA3TPOQQG65TFOIQSAWLPOUQG2YLZEBUGC5TFEBZWC5TFMQQHS33VOIQGEZLMN53GKZBAOBWGC3TFOQQHI2DJOMQHI2LNMUWCASDBMNVWK4RNNVQW4LBAMJ2XIICJEB3WS3DMEBRGKIDCMFRWWIDXNF2GQIDBEBRGSZ3HMVZCYIDNN5ZGKIDEMFZXIYLSMRWHSIDQNRQW4IDUN4QGOZLUEBZGSZBAN5TCA5DIMF2CA2LOMZSXE2LPOIQG64DFOJQXI2LOM4QHG6LTORSW2LBAJRUW45LYFYQA====

4\. Decode from Base32



Press enter or click to view image in full size



cyberchef

What is the root flag?



flag{iteeKdbu==hjK6Â§YuUu7-6N\_}

