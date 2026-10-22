Gobuster
Gobuster is an open-source tool written in Go that is used to brute-force URIs (directories and files) in websites, DNS subdomains, virtual host names on target web servers, and open Amazon S3 buckets. Its speed and efficiency make it a preferred choice among security professionals for reconnaissance and enumeration tasks.

Here are the primary uses of Gobuster:

Directory and File Enumeration: Gobuster excels at discovering hidden directories and files on web servers by brute-forcing URIs using wordlists. This capability helps security professionals identify potential entry points and exposed resources that may not be linked from the main website.

DNS Subdomain Enumeration: The tool can perform DNS subdomain enumeration to discover subdomains associated with a target domain. This feature is crucial during the reconnaissance phase of penetration testing to map out the complete attack surface of an organization.

Virtual Host Discovery: Gobuster can enumerate virtual hosts on a web server, revealing multiple websites hosted on the same IP address. This functionality helps identify all web applications associated with a target infrastructure.

S3 Bucket Enumeration: It includes functionality to enumerate Amazon S3 buckets, helping identify publicly accessible cloud storage that may contain sensitive information or misconfigurations that could be exploited.

High Performance: Written in Go and utilizing goroutines, Gobuster provides exceptional speed and efficiency. It can handle multiple concurrent requests, making it significantly faster than many alternative tools for similar tasks.

Flexibility and Customization: Gobuster offers various modes and options that allow users to customize their scans according to specific requirements, including custom headers, authentication, proxy support, and pattern matching.

Core Features
High-Speed Scanning
Multiple Enumeration Modes
Directory and File Brute-forcing
DNS Subdomain Enumeration
Virtual Host Discovery
S3 Bucket Enumeration
Wildcard Detection
Custom Wordlist Support
Pattern Matching and Filtering
Proxy and Authentication Support
Recursive Scanning
Custom HTTP Headers
Data sources
Wordlists
Target URLs
DNS Resolvers
HTTP Response Codes
Response Content
DNS Records
Virtual Host Configurations
S3 Bucket Names
Common Gobuster Commands
### 1. Directory Enumeration (Basic)
This command performs basic directory enumeration on the target URL using the specified wordlist. It discovers hidden directories and files on the web server.
gobuster dir -u http://example.com -w /path/to/wordlist.txt

###  2. Specify File Extensions
This command searches for files with specific extensions during directory enumeration. It helps identify specific file types like PHP, HTML, or configuration files on the target server.
gobuster dir -u http://example.com -w /path/to/wordlist.txt -x php,html,txt

### 3. DNS Subdomain Enumeration
This command discovers subdomains of the target domain using DNS enumeration. It helps map the complete subdomain structure of an organization's online presence.
gobuster dns -d example.com -w /path/to/subdomains.txt

### 4. Virtual Host Discovery
This command enumerates virtual hosts on a target server. It reveals multiple websites or applications hosted on the same IP address or server infrastructure.
gobuster vhost -u http://example.com -w /path/to/vhosts.txt

### 5. S3 Bucket Enumeration
This command searches for publicly accessible Amazon S3 buckets using the provided wordlist. It helps identify potential data exposure through misconfigured cloud storage.
gobuster s3 -w /path/to/bucket-names.txt

### 6. Custom Status Codes
This command filters results to display only responses with specific HTTP status codes. It allows users to focus on particular response types during enumeration.
gobuster dir -u http://example.com -w /path/to/wordlist.txt -s 200,204,301,302,307,401


### 7. Add Custom Headers
This command adds custom HTTP headers to requests. It's useful for bypassing certain security controls or providing authentication tokens during enumeration.
gobuster dir -u http://example.com -w /path/to/wordlist.txt -H "Authorization: Bearer token"


### 8. Use Proxy
This command routes all requests through a specified proxy server. It's essential for traffic analysis, authentication, or bypassing network restrictions.
gobuster dir -u http://example.com -w /path/to/wordlist.txt --proxy http://127.0.0.1:8080


### 9. Recursive Enumeration
This command enables recursive scanning, automatically enumerating subdirectories found during the initial scan. It provides comprehensive directory structure mapping.
gobuster dir -u http://example.com -w /path/to/wordlist.txt -r

### 10. Timeout and Threads Configuration
This command sets custom timeout values and thread count for the scan. It allows optimization of scan speed while avoiding server overload or detection.
gobuster dir -u http://example.com -w /path/to/wordlist.txt -t 50 --timeout 10s

### 11. Exclude Response Length
This command excludes results based on response length, filtering out false positives or uninteresting results based on content size.
gobuster dir -u http://example.com -w /path/to/wordlist.txt --exclude-length 1234

### 12. Output to File
This command saves the scan results to a specified output file. It facilitates post-scan analysis and integration with other security tools.
gobuster dir -u http://example.com -w /path/to/wordlist.txt -o results.txt

### 13. Help and Usage Information
This command displays the help menu and usage information for Gobuster, listing all available options and modes.
gobuster -h

Alternative usage:

### gobuster --help

Output Examples of Gobuster Commands
Command	Example Usage	Function	Output Example
Directory Enumeration	gobuster dir -u http://example.com -w wordlist.txt	Performs basic directory enumeration.	http://example.com/admin (Status: 200) [Size: 1234]
Specify File Extensions	gobuster dir -u http://example.com -w wordlist.txt -x php,html	Searches for files with specific extensions.	http://example.com/index.php (Status: 200)
Custom Status Codes	gobuster dir -u http://example.com -w wordlist.txt -s 200,301	Filters results by HTTP status codes.	http://example.com/backup (Status: 301)
DNS Subdomain Enumeration	gobuster dns -d example.com -w subdomains.txt	Discovers subdomains via DNS enumeration.	Found: admin.example.com
Virtual Host Discovery	gobuster vhost -u http://example.com -w vhosts.txt	Enumerates virtual hosts on the server.	Found: dev.example.com (Status: 200)
S3 Bucket Enumeration	gobuster s3 -w bucket-names.txt	Searches for accessible S3 buckets.	http://example-bucket.s3.amazonaws.com (Status: 200)
Add Custom Headers	gobuster dir -u http://example.com -w wordlist.txt -H "X-Custom: value"	Adds custom HTTP headers to requests.	Using custom header: X-Custom
Use Proxy	gobuster dir -u http://example.com -w wordlist.txt --proxy http://127.0.0.1:8080	Routes requests through a proxy.	Using proxy: http://127.0.0.1:8080
Recursive Scanning	gobuster dir -u http://example.com -w wordlist.txt -r	Enables recursive directory scanning.	http://example.com/admin/users (Status: 200)
Wildcard Detection	gobuster dir -u http://example.com -w wordlist.txt --wildcard	Detects and handles wildcard responses.	Wildcard response detected: disabling wildcards
Follow Redirects	gobuster dir -u http://example.com -w wordlist.txt -r	Follows HTTP redirects automatically.	http://example.com/old → http://example.com/new
Set Threads	gobuster dir -u http://example.com -w wordlist.txt -t 50	Sets the number of concurrent threads.	Using 50 threads
Set Timeout	gobuster dir -u http://example.com -w wordlist.txt --timeout 10s	Sets request timeout duration.	Timeout set to 10 seconds
Exclude Length	gobuster dir -u http://example.com -w wordlist.txt --exclude-length 1234	Excludes responses with specific length.	Excluding responses of length 1234
Pattern Matching	gobuster dir -u http://example.com -w wordlist.txt -p pattern.txt	Uses pattern file for enumeration.	Using pattern file: pattern.txt
No Status Codes	gobuster dir -u http://example.com -w wordlist.txt -n	Disables status code display.	http://example.com/admin
No Progress Bar	gobuster dir -u http://example.com -w wordlist.txt -q	Disables progress bar output.	http://example.com/admin (Status: 200)
Verbose Output	gobuster dir -u http://example.com -w wordlist.txt -v	Enables verbose output mode.	[+] Mode: dir
[+] Url: http://example.com
Output to File	gobuster dir -u http://example.com -w wordlist.txt -o output.txt	Saves results to a file.	Results saved to output.txt
Username Enumeration	gobuster dir -u http://example.com -w wordlist.txt -U username -P password	Provides credentials for authentication.	Using basic authentication: username
User-Agent String	gobuster dir -u http://example.com -w wordlist.txt -a "Mozilla/5.0"	Sets custom User-Agent header.	Using User-Agent: Mozilla/5.0
Cookies	gobuster dir -u http://example.com -w wordlist.txt -c "session=abc123"	Adds cookies to requests.	Using cookies: session=abc123
No TLS Verification	gobuster dir -u https://example.com -w wordlist.txt -k	Skips TLS certificate verification.	Skipping TLS verification
DNS Resolver	gobuster dns -d example.com -w wordlist.txt -r 8.8.8.8	Uses custom DNS resolver.	Using DNS resolver: 8.8.8.8
Show IPs	gobuster dns -d example.com -w wordlist.txt -i	Displays IP addresses in DNS mode.	admin.example.com [192.168.1.1]
Show CNAMEs	gobuster dns -d example.com -w wordlist.txt --show-cname	Displays CNAME records in DNS mode.	www.example.com → cdn.example.com