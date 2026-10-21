**WELCOME TO LAYOVER LAB**



**###   NMAP COMMAND**

**1. Initial Enumeration**

**I started with a standard service enumeration using Nmap.**



**The command used was nmap -sC -sV <TARGET\_IP>.**



**The scan revealed two important services:**



**TCP/22 — SSH**

**TCP/3389 — RDP**

**SSH was interesting, but RDP immediately stood out because it provided access to an actual workstation.**



**The initial credentials supplied by Hack The Box were used only for the intended RDP access and are intentionally not included here.**



**The important observation at this stage was that the target exposed a Windows remote desktop service that could potentially provide access to networks unavailable directly from Kali.**







**2. RDP Access**

**I connected to the target using an RDP client.**



**The workstation hostname was identified as airside-ws01.**



**Once inside the workstation, I began enumerating the local environment instead of immediately attacking the externally exposed SSH service.**



**The first things worth checking after obtaining access to a workstation are:**



**Network interfaces**

**Routing table**

**Wireless adapters**

**DNS configuration**

**Local users**

**Running services**

**Available security/network tools**

**This quickly revealed that the workstation had more than one network interface.**



**That discovery became extremely important.**



**3. Discovering the Internal Network**

**The workstation had access to a wireless network that was initially not being used.**



**Network configuration can be examined with commands such as ip addr and ip route.**



**Wireless configuration can also be investigated with nmcli device status and nmcli device wifi list.**



**An internal wireless network named HTB International WiFi was identified.**



**After connecting the appropriate wireless interface, the workstation obtained an internal network route.**



**The internal network was in the 10.13.37.0/24 range.**



**This was a major turning point.**



**The internal web infrastructure was not part of the original external attack surface. The compromised workstation effectively provided a route into that internal environment.**



**4. Wireless Traffic Analysis**

**With access to the internal wireless environment, I investigated the available wireless traffic.**



**The traffic contained useful authentication information.**



**Instead of blindly brute-forcing the internal application, I analyzed the available traffic and authentication exchanges.**



**Tools such as Wireshark and tshark are useful for this type of investigation.**



**The analysis eventually revealed credentials for an internal application account.**



**The actual username and password are intentionally omitted from this write-up.**



**This credential discovery provided the next step toward the internal web application.**





**5. Internal Web Portal**

**After establishing the internal network connection, I investigated the internal web infrastructure.**



**The primary application was hosted at portal.international.htb.**



**The Miles application was available through /miles/login.php.**



**The credentials recovered during the wireless investigation allowed authenticated access to the application.**



**Further enumeration revealed an administrative interface at /admin.**



**The administrative interface identified the underlying CMS as Craft CMS.**



**The installed version was Craft CMS 5.9.8.**



**At this point, version enumeration became very important because the next stage depended on a vulnerability affecting the installed CMS version.**







**6. Craft CMS Remote Code Execution**

**The vulnerable functionality was associated with the Craft CMS element-search functionality.**



**The relevant endpoint was:**



**/admin/actions/element-search/search**



**The installation was vulnerable to authenticated remote code execution through the affected functionality.**



**Because valid application credentials had already been obtained, the vulnerable functionality could be reached.**



**A public proof-of-concept was used to verify the vulnerability.**



**The check confirmed that remote command execution was possible.**



**The resulting shell executed as:**



**www-data**



**This was the first operating-system-level foothold on the internal Linux server.**





**7. Enumerating the Web Application**

**Once command execution was obtained, I started enumerating the application from the perspective of www-data.**



**The main application directory was:**



**/var/www/portal**



**The first important file discovered was:**



**/var/www/portal/.env**



**Environment files are particularly interesting during web application assessments because they frequently contain:**



**Database credentials**

**Application secrets**

**Encryption keys**

**API keys**

**Debug configuration**

**Internal service information**

**In this case, the .env file exposed the Craft security configuration and database connection information.**



**The actual secret values are intentionally omitted.**



**The database configuration indicated that the application used MySQL locally.**





**8. Database Backup**

**The application’s storage directory contained a database backup.**



**The backup was located under:**



**/var/www/portal/storage/backups/**



**After extracting the database, I began examining the available tables.**



**One interesting table was miles\_members.**



**It contained application-specific passenger/member information.**



**However, it did not directly provide the Linux user’s password.**



**This was an important lesson.**



**Finding a database backup does not necessarily mean that the required credential will be sitting inside a normal users table.**



**When one avenue doesn’t provide the required information, the application source code can often explain how sensitive values are actually being stored or processed.**



**9. Investigating Custom Application Code**

**Further enumeration revealed a custom Craft module associated with the HTB Airways functionality.**



**One particularly interesting file was:**



**/var/www/portal/modules/htbairways/console/controllers/MilesController.php**



**The source code showed that a setting called mailRelayPassword was stored as an encrypted value.**



**More importantly, the source code showed exactly how the application decrypted it.**



**The application retrieved the Craft security key and passed the encrypted value through Craft’s own decryption functionality.**



**Conceptually, the process was:**



**Encrypted database value + Craft security key + application decryption logic = recoverable secret**



**This was the key discovery that connected the application configuration and database information to the next system-level account.**



**The recovered credential itself is intentionally omitted.**



**10. Pivoting to a Linux User**

**The application source code revealed that the mail-relay configuration was associated with a Linux account.**



**I verified that the corresponding account existed on the operating system.**



**This distinction is important because application usernames and Linux usernames should never automatically be assumed to be the same account.**



**The account was confirmed using normal Linux account enumeration.**



**At this point, the next logical step was to determine whether the recovered credential could be used for SSH access.**



**11. SSH Access**

**SSH was already identified during the initial Nmap scan.**



**After the internal network route was established and the appropriate credential had been recovered, SSH access to the internal server became possible.**



**The connection followed the standard format:**



**ssh <USERNAME>@<INTERNAL\_IP>**



**The actual username/password combination is intentionally omitted.**



**After logging in, I verified the new shell using commands such as whoami and id.**



**This provided a proper Linux user shell rather than the restricted web-server context.**



**12. Local Enumeration**

**After obtaining a normal Linux user shell, I restarted enumeration.**



**Important checks included:**



**id**



**whoami**



**sudo -l**



**uname -a**



**ps aux**



**ss -lntup**



**and running services through systemctl.**



**The objective at this stage was to identify:**



**Privileged processes**

**Interesting services**

**Vulnerable software versions**

**SUID binaries**

**Scheduled jobs**

**Writable configuration files**

**Local network services**

**One service immediately stood out:**



**CUPS — the Common UNIX Printing System.**



**13. CUPS Enumeration**

**The CUPS service was running locally.**



**The daemon was cupsd.**



**The service was listening on the local CUPS port:**



**127.0.0.1:631**



**The next step was to identify the exact installed version.**



**The version can be checked with:**



**cups-config --version**



**The machine was running:**



**CUPS 2.4.16**



**This version was significant because it fell within the affected range for CVE-2026–34990.**



**14. Verifying the Exploitation Environment**

**Before running a privilege-escalation PoC, I checked whether the target contained the required utilities.**



**For example:**



**which ipptool**



**python3 --version**



**which socat**



**which nc**



**The necessary components were available.**



**This is an important practical step.**



**Rather than immediately running a PoC, it is better to verify:**



**The target version is vulnerable.**

**The exploit actually targets that version.**

**Required dependencies exist.**

**The exploit file is the correct one.**

**The exploit is syntactically valid.**

**15. Obtaining the Correct CUPS PoC**

**The target did not have the required external Internet access, so the CUPS proof-of-concept was obtained separately and transferred to the internal machine.**



**An important problem occurred during this stage.**



**There were multiple files named exploit.py during the engagement.**



**One exploit.py belonged to the Craft CMS exploitation stage.**



**The CUPS vulnerability required a completely different PoC.**



**This is a very useful real-world lesson:**



**Never assume that a file called exploit.py is the exploit you need.**



**Always inspect the repository, README, imports, target software, and vulnerability identifier before executing it.**



**16. Verifying the PoC**

**After transferring the correct CUPS PoC to the target, I first checked the file.**



**The file size and location were verified using ls -lh.**



**Then Python syntax was checked using:**



**python3 -m py\_compile /tmp/exploit.py**



**The syntax check completed successfully.**



**This is a simple step, but it can prevent wasting time debugging a corrupted or incorrectly transferred exploit.**



**17. CVE-2026–34990 Exploitation**

**The CUPS PoC was then executed from the local user shell.**



**The exploitation process involved manipulating local IPP communication with CUPS.**



**At a high level, the exploit performed the following sequence:**



**Local rogue IPP server → CUPS interaction → authorization token capture → privileged printer operation → file operation → sudoers modification**



**The PoC ultimately created a sudoers configuration under:**



**/etc/sudoers.d/**



**The exploit then verified privileged execution.**



**The resulting execution context was UID 0.**



**This demonstrated successful local privilege escalation.**



**18. Root Access**

**After successful exploitation, a root shell could be obtained.**



**The important confirmation was:**



**uid=0(root)**



**At this point, the complete privilege chain had been established:**



**Web access → www-data → Linux user → root**



**The root flag is intentionally omitted from this write-up.**



**19. Vulnerability Summary**

**ComponentVersionSecurity ImpactCraft CMS5.9.8Authenticated Remote Code ExecutionCUPS2.4.16Local Privilege EscalationWireless environmentInternalCredential exposureApplication configuration.envSensitive secret exposureApplication sourceCustom moduleRevealed secret-decryption logic**



**20. Complete Attack Path**

**1. Initial Nmap enumeration**



**The target exposed SSH and RDP.**



**↓**



**2. RDP access**



**The provided HTB credentials allowed access to the workstation.**



**↓**



**3. Local network enumeration**



**Multiple interfaces were discovered.**



**↓**



**4. Internal wireless network**



**The workstation could connect to the internal wireless environment.**



**↓**



**5. Wireless traffic analysis**



**Authentication information was recovered from the available traffic.**



**↓**



**6. Internal portal**



**The recovered credentials provided access to the internal web application.**



**↓**



**7. Craft CMS discovery**



**The application was identified as Craft CMS 5.9.8.**



**↓**



**Become a Medium member**

**8. Authenticated RCE**



**The vulnerable Craft functionality provided command execution.**



**↓**



**9. www-data**



**The initial Linux foothold was obtained as the web-server account.**



**↓**



**10. Application enumeration**



**The .env, database backup, and application source were investigated.**



**↓**



**11. Credential recovery**



**Application source code revealed how an encrypted credential was decrypted.**



**↓**



**12. Linux user**



**The recovered credential provided access to a normal Linux account.**



**↓**



**13. SSH**



**A proper SSH shell was obtained.**



**↓**



**14. Local enumeration**



**Running services were investigated.**



**↓**



**15. CUPS**



**CUPS 2.4.16 was identified.**



**↓**



**16. CVE-2026–34990**



**The vulnerable CUPS installation was exploited for local privilege escalation.**



**↓**



**17. Root**



**UID 0 execution was obtained.**



**21. Lessons Learned**

**RDP can be more valuable than an exposed SSH service**

**The first exposed service wasn’t necessarily the final attack path.**



**The RDP workstation provided access to an internal network that wasn’t directly available from the attacking machine.**



**Always check network interfaces and routes**

**After gaining access to another machine, immediately check:**



**ip addr**



**and:**



**ip route**



**You may discover an entirely different network.**



**Don’t ignore wireless interfaces**

**A disconnected wireless interface can still be extremely important.**



**In this machine, reconnecting to the internal wireless network changed the available attack surface completely.**



**Database backups deserve serious attention**

**Backups can contain:**



**Application data**

**Configuration**

**API keys**

**Credentials**

**Encryption-related information**

**Historical application state**

**Even when the desired password isn’t directly present, the backup can reveal how the application works.**



**Source code can be more valuable than the database itself**

**The database contained an encrypted value.**



**The application source code explained how that value was decrypted.**



**That combination transformed an apparently useless encrypted value into useful authentication information.**



**Don’t confuse application users with Linux users**

**A username found in a web application’s database does not automatically represent an operating-system account.**



**Always verify the account with Linux enumeration.**



**Restart enumeration after every privilege change**

**Enumeration should happen at every stage:**



**RDP → web application → www-data → Linux user → root**



**The available information changes significantly after each pivot.**



**Version enumeration is critical**

**The CUPS version was the key piece of information that connected the local service to the applicable privilege-escalation vulnerability.**



**Always identify exact versions before searching for exploits.**



**Verify PoCs before running them**

**During the engagement, multiple exploit files had similar names.**



**Checking the contents of the file and confirming the vulnerability it targets prevented using the wrong PoC.**



**This is especially important when working with multiple vulnerabilities in the same machine.**



**22. Final Takeaway**

**Layover is a good example of a multi-stage attack chain rather than a machine solved by a single vulnerability.**



**The important progression was:**



**RDP**



**↓**



**Internal Network**



**↓**



**Wireless Traffic Analysis**



**↓**



**Internal Credentials**



**↓**



**Craft CMS**



**↓**



**Authenticated RCE**



**↓**



**www-data**



**↓**



**Application Configuration + Database + Source Code**



**↓**



**Linux User**



**↓**



**SSH**



**↓**



**CUPS 2.4.16**



**↓**



**CVE-2026–34990**



**↓**



**Root**



**The biggest lesson from the machine is to keep enumerating after every foothold. The initial RDP access, internal network, web application, application source code, Linux account, and local CUPS service all looked like separate pieces, but together they formed the complete path to root.**



**Tools Used**

**Nmap**

**xfreerdp**

**ip**

**nmcli**

**Wireshark**

**tshark**

**Browser**

**Craft CMS enumeration**

**Python**

**SSH**

**Linux enumeration utilities**

**CUPS utilities**

**No passwords, recovered credentials, user flag, or root flag are included in this version.**

**Beginner Hints**



**Stuck on Layover? Try these hints in order. Don’t jump to the last one immediately!**



**Hint 1 — Start with Enumeration**

**Don’t assume the machine is only about SSH.**



**Start by identifying all exposed services and their versions.**



**Think:**



**What services are accessible from my attacking machine?**



**Hint 2 — Look Beyond the Initial Target**

**If you obtain access to a workstation, don’t immediately start brute-forcing passwords.**



**Check:**



**ip addr**



**and:**



**ip route**



**Ask yourself:**



**Does this machine have access to another network?**



**Hint 3 — Investigate Wireless**

**If you see a wireless interface, investigate it.**



**Useful questions:**



**What wireless interfaces exist?**

**Is one disconnected?**

**What networks are visible?**

**Can the workstation connect to an internal network?**

**Does the routing table change after connecting?**

**Hint 4 — Don’t Ignore Traffic**

**Once you’re on the internal network, think about what traffic is already happening.**



**Wireshark can help you inspect:**



**HTTP**

**DNS**

**TCP**

**Authentication traffic**

**Cleartext credentials**

**Ask yourself:**



**Is someone already authenticating somewhere?**



**Hint 5 — Enumerate the Internal Web Application**

**Once you discover an internal web server, don’t just browse the homepage.**



**Look for:**



**Login pages**

**Admin panels**

**Interesting directories**

**Technology fingerprints**

**CMS names**

**Version numbers**

**A useful question is:**



**What software is running behind this website?**



**Hint 6 — Version Numbers Matter**

**If you identify a CMS, don’t stop at the name.**



**For example:**



**Craft CMS**



**isn’t enough.**



**You want:**



**Craft CMS + exact version**



**Then investigate whether that version has known vulnerabilities.**



**Hint 7 — After Getting RCE, Slow Down**

**Getting www-data does not mean you're finished.**



**Start local enumeration.**



**Look at:**



**/var/www/**



**/var/www/<application>/**



**.env**



**configuration files**



**backups**



**source code**



**custom modules**



**Ask:**



**What secrets did the developer accidentally leave behind?**



**Hint 8 — Encrypted Doesn’t Always Mean Unrecoverable**

**If you discover something like:**



**encrypted\_password = <blob>**



**don’t immediately give up.**



**Look for:**



**Encryption/decryption functions**

**Application keys**

**Environment variables**

**Configuration files**

**Source code**

**The important question is:**



**How does the application itself decrypt this value?**



**Hint 9 — Think About Credential Reuse**

**If you recover a credential associated with an application service, don’t automatically assume it is useless for Linux.**



**Check whether the related username exists on the operating system.**



**Think about possible reuse between:**



**Application → Service → Linux account → SSH**



**Hint 10 — Re-Enumerate After SSH**

**Once you get a real Linux shell, start enumeration again.**



**Check:**



**id**



**sudo -l**



**ps aux**



**ss -lntup**



**running services**



**installed software versions**



**Don’t rely only on the enumeration you performed as www-data.**



**Hint 11 — Look at Local Services**

**Some privilege-escalation paths aren’t exposed through Nmap.**



**A service might only be listening on:**



**127.0.0.1**



**but still be exploitable locally.**



**Ask:**



**What privileged services are running on the machine?**



**Hint 12 — Check Exact Versions**

**If you discover an interesting service, identify its exact version.**



**For example:**



**CUPS → version**



**Then search for vulnerabilities affecting that specific version.**



**Don’t blindly run random exploits.**



**Hint 13 — Verify the PoC**

**Before executing an exploit, confirm:**



**Does it target the correct software?**

**Does it target the correct version?**

**Are its dependencies available?**

**Is this actually the exploit I intended to run?**

**A file named exploit.py doesn't tell you what vulnerability it exploits.**



















