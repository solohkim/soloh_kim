Gobuster is a popular tool written in “Go”, and it’s used for directory, file, and DNS brute-forcing. It’s commonly used in penetration testing and security assessments to discover hidden resources on a web server or enumerate subdomains.

![scan](/tools/images/gobuster1.png)


### Installation

sudo apt-get install gobuster

Usage
Gobuster operates in different modes: directory/file brute-forcing, DNS subdomain brute-forcing, virtual host brute-forcing, and S3 bucket enumeration.

### 1. Directory/File Brute-Forcing

To discover hidden directories and files on a web server:

```bash
gobuster dir -u http://example.com -w /path/to/wordlist.txt

```

dir: Specifies directory brute-forcing mode.
-u: Specifies the target URL.
-w: Specifies the path to the wordlist


Common Options:

-e: Expanded mode, prints full URLs.
-x: Specifies file extensions to search for (e.g., -x, txt, php, html).
-t: Number of concurrent threads (default is 10).
-r: Follow redirects. (ex: searching from example.com/* to example.com/admin/* after finding “/admin/”)
-s: Positive status codes (default: 


### Example:

```bash
gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/common.txt -x .php,.html -t 20
```


### 2. DNS Subdomain Brute-Forcing

To find subdomains of a given domain:


```bash
gobuster dns -d example.com -w /path/to/wordlist.txt
```

dns: Specifies DNS brute-forcing mode.
-d: Specifies the target domain.
-w: Specifies the path to the wordlist.
Common Options:

-i: Show IPs of resolved subdomains.
-t: Number of concurrent threads (default is actually 10).
-r: Use a specific DNS server (e.g., -r 8.8.8.8).
Example:

gobuster dns -d 

example.com -w…


