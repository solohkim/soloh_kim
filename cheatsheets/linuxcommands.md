When it comes to managing a Linux server, mastering the Linux server commands on the command line is crucial. The command line interface (CLI) provides powerful tools that allow system administrators to perform tasks quickly, efficiently, and with a high degree of control. Whether you’re configuring network settings, managing users, or optimizing performance, knowing the right Linux server commands can save time and prevent errors.

In this comprehensive guide, we’ll explore 100 of the most important Linux server commands, organized into key categories that cover everything from basic file management to advanced system administration. Whether you’re a seasoned sysadmin or a newcomer to Linux, this guide will help you become more proficient in managing your server environment.

Basic Commands
Basic commands are the foundation of working with Linux servers. They are essential for navigating the file system, handling files and directories, and performing day-to-day tasks on the command line. Here, we’ll discuss the most important basic commands that every Linux system administrator should be familiar with.

### 1. pwd (Print Working Directory)
Usage: pwd
Description: Displays the current directory path. This command is helpful when you want to know the exact location within the file system where you’re working. For example, if you’re deep inside nested directories, pwd will show the full path.
### 2. ls (List Directory Contents)
Usage: ls [options] [directory]
Description: Lists the files and directories in the current directory. Common options include:
-l for a detailed list (shows permissions, ownership, size, etc.).
-a to include hidden files.
-h for human-readable file sizes.
### 3. cd (Change Directory)
Usage: cd [directory]
Description: Changes the current directory to the specified directory. For instance, cd /home/user/documents navigates to the “documents” directory. Use cd .. to move up one directory level, and cd ~ to go to the home directory.
### 4. mkdir (Make Directory)
Usage: mkdir [directory name]
Description: Creates a new directory with the specified name. For example, mkdir newfolder creates a directory called “newfolder” in the current location.
### 5. rm (Remove Files or Directories)
Usage: rm [options] [file or directory]
Description: Deletes files or directories. Important options include:
-r for recursive deletion (necessary for directories).
-f to force deletion without prompts.
Caution: Be very careful with rm -rf, as it will delete everything in the specified directory without asking for confirmation.
### 6. cp (Copy Files or Directories)
Usage: cp [source] [destination]
Description: Copies files or directories from one location to another. Use the -r option to copy directories recursively. For example, cp -r folder1 folder2 copies “folder1” to “folder2”.
### 7. mv (Move or Rename Files or Directories)
Usage: mv [source] [destination]
Description: Moves files or directories to a different location, or renames them if the destination is within the same directory. For instance, mv oldname newname renames a file.
### 8. touch (Create an Empty File or Update File Timestamps)
Usage: touch [file name]
Description: Creates an empty file with the specified name if it doesn’t exist, or updates the modification and access time of the file if it does. This is useful for creating placeholder files or updating timestamps.
### 9. cat (Concatenate and Display File Contents)
Usage: cat [file]
Description: Displays the content of a file. For example, cat example.txt will output the contents of “example.txt” to the terminal. You can also concatenate multiple files using cat file1 file2 > combinedfile.
### 10. echo (Display a Line of Text)
Usage: echo [text]
Description: Outputs the specified text to the terminal. It is often used in scripts to display messages or to write text to files, e.g., echo “Hello, World!” > hello.txt writes “Hello, World!” to the file “hello.txt”.
These basic commands form the core of Linux command-line operations. They allow you to navigate through the file system, manage files and directories, and perform simple tasks that are essential for more complex system administration.

Also Check: Migrating from Windows Server to Linux: Best Practices and Considerations

File and Directory Management
File and directory management commands are crucial for organizing, searching, and manipulating files and directories on a Linux server. These commands give you control over file permissions, ownership, and content, allowing you to efficiently manage your server’s file system.

### 11. chmod (Change File Modes or Access Permissions)
Usage: chmod [options] [permissions] [file or directory]
Description: Changes the access permissions of files or directories. Permissions can be set using symbolic (e.g., chmod u+x file) or numeric (e.g., chmod 755 file) modes. This command is essential for controlling who can read, write, or execute files.
### 12. chown (Change File Owner and Group)
Usage: chown [owner][:group] [file or directory]
Description: Changes the ownership of files or directories. For example, chown user:group file sets the file’s owner to “user” and its group to “group”. This is important for managing access control on multi-user systems.
### 13. find (Search for Files in a Directory Hierarchy)
Usage: find [path] [options] [expression]
Description: Searches for files and directories within a specified path that match a given expression. For example, find /home/user -name “*.txt” searches for all .txt files in the user’s home directory. This command is highly versatile, allowing you to search by name, type, size, modification time, and more.
### 14. grep (Search for Text Patterns in Files)
Usage: grep [options] [pattern] [file]
Description: Searches for a specific pattern of text within files. For example, grep “error” logfile.txt will return all lines in “logfile.txt” that contain the word “error”. This command is invaluable for quickly finding specific information within large files.
### 15. tar (Archive Files)
Usage: tar [options] [archive name] [file or directory]
Description: Creates and extracts archive files. Common options include:
-c to create a new archive.
-x to extract an archive.
-v for verbose output.
-f to specify the file name of the archive.
-z to compress the archive using gzip.
For example, tar -czvf archive.tar.gz folder creates a compressed archive of “folder”.
### 16. zip / unzip (Compress and Decompress Files)
Usage: zip [archive name] [file or directory] / unzip [archive name]
Description: zip compresses files into a ZIP archive, while unzip extracts them. For instance, zip -r archive.zip folder creates a ZIP archive of “folder”, and unzip archive.zip extracts it.
### 17. ln (Create Hard and Symbolic Links)
Usage: ln [options] [target] [link name]
Description: Creates links to files. A hard link points directly to the inode of the original file, while a symbolic link (or symlink) is a pointer to another file or directory. For example, ln -s /path/to/file linkname creates a symlink to “file”.
### 18. df (Report File System Disk Space Usage)
Usage: df [options]
Description: Displays the amount of disk space used and available on mounted file systems. The -h option provides human-readable output, showing sizes in KB, MB, or GB. This command is essential for monitoring disk usage on your server.
19. du (Estimate File Space Usage)
Usage: du [options] [file or directory]
Description: Summarizes disk usage of each file or directory. For example, du -sh folder shows the total size of “folder” in a human-readable format. This command helps identify which directories are consuming the most space.
20. rsync (Remote File and Directory Synchronization)
Usage: rsync [options] [source] [destination]
Description: Efficiently synchronizes files and directories between two locations, either locally or remotely. For example, rsync -avz /source/ user@remote:/destination/ syncs files from a local source to a remote destination with compression. rsync is widely used for backups and mirroring.
File and directory management commands are vital for maintaining order and ensuring efficient storage management on a Linux server. These commands provide the tools needed to search, organize, and manage files and directories effectively, ensuring that your server runs smoothly and that files are easily accessible when needed.

System Information
System information commands are essential for gathering details about the system’s hardware, software, and overall performance. These commands help administrators monitor the system’s status, diagnose issues, and make informed decisions about system management and resource allocation.

21. uname (Print System Information)
Usage: uname [options]
Description: Displays system information, such as the kernel name, version, and machine hardware name. Common options include:
-a for all information.
-r for the kernel version.
For example, uname -r outputs the kernel version.
22. top (Display Linux Tasks)
Usage: top
Description: Provides a dynamic, real-time view of running processes, including their CPU and memory usage. It’s an essential tool for monitoring system load and identifying resource-hungry processes. You can sort processes by CPU or memory usage, kill processes, and more directly from the top interface.
23. htop (Interactive Process Viewer)
Usage: htop
Description: Similar to top, but with an enhanced user interface that allows for easier navigation and interaction. htop provides color-coded, real-time information about system processes, making it easier to monitor and manage them.
24. df (Report File System Disk Space Usage)
Usage: df [options]
Description: Shows the amount of disk space used and available on all mounted file systems. The -h option provides a human-readable format, displaying sizes in KB, MB, or GB. This command is crucial for monitoring and managing disk space on your server.
25. du (Estimate File Space Usage)
Usage: du [options] [file or directory]
Description: Summarizes disk usage of files and directories. Use the -sh option to get a human-readable summary of a directory’s size. For instance, du -sh /var/log shows the total size of the /var/log directory. This command helps identify which directories or files are consuming the most disk space.
26. free (Display Memory Usage)
Usage: free [options]
Description: Shows the amount of free and used memory in the system. The -h option displays the output in a human-readable format (MB, GB). For example, free -h provides an overview of total, used, and available memory, as well as swap usage.
27. uptime (Tell How Long the System Has Been Running)
Usage: uptime
Description: Displays the current time, how long the system has been running, the number of users currently logged in, and the system load averages for the past 1, 5, and 15 minutes. This command is useful for quickly checking the system’s stability and load.
28. hostname (Show or Set the System’s Host Name)
Usage: hostname [options] [name]
Description: Displays or sets the system’s host name. Running hostname without any options shows the current host name, while hostname newname sets a new host name. This is important for identifying the server on a network.
29. uname -r (Display Kernel Version)
Usage: uname -r
Description: Outputs the version of the Linux kernel currently running on the system. This is crucial for troubleshooting and ensuring compatibility with software and drivers.
30. vmstat (Report Virtual Memory Statistics)
Usage: vmstat [options] [delay [count]]
Description: Provides detailed information about processes, memory, paging, block I/O, traps, and CPU activity. For example, vmstat 5 3 displays memory statistics at 5-second intervals, three times. This command is particularly useful for identifying memory bottlenecks.
31. iostat (Report CPU and I/O Statistics)
Usage: iostat [options] [delay [count]]
Description: Provides detailed reports on CPU and I/O statistics, helping to identify performance issues related to disk I/O. For example, iostat 5 displays statistics every 5 seconds. This command is essential for diagnosing performance problems in storage systems.
System information commands are indispensable for monitoring and diagnosing the health and performance of your Linux server. By using these commands, you can gather crucial data about the system’s status, identify potential issues, and make informed decisions to ensure optimal server performance.

Recommended Reading: Why Linux is the Ultimate Alternative to Windows Server

Network Management
Network management commands are critical for configuring, troubleshooting, and monitoring network interfaces and connectivity on a Linux server. These commands help ensure that your server is properly connected to the network and can communicate effectively with other devices.

32. ping (Send ICMP ECHO_REQUEST to Network Hosts)
Usage: ping [options] [destination]
Description: Tests the network connectivity between your server and another device by sending ICMP ECHO_REQUEST packets and measuring the response time. For example, ping google.com checks if your server can reach Google and how long it takes. It’s a fundamental tool for diagnosing network connectivity issues.
33. ifconfig (Configure Network Interfaces)
Usage: ifconfig [interface] [options]
Description: Displays or configures network interfaces. For example, ifconfig eth0 shows the configuration of the eth0 interface. Although largely replaced by the ip command in modern systems, ifconfig is still commonly used for viewing and setting IP addresses, subnet masks, and enabling/disabling interfaces.
34. ip (Show/Manipulate Routing, Devices, and Tunnels)
Usage: ip [options] [object]
Description: A more modern and powerful tool than ifconfig for configuring network interfaces, routing, and tunnels. For example, ip addr show displays all network interfaces and their associated IP addresses. The ip command suite is versatile and crucial for advanced network configuration.
35. netstat (Network Statistics)
Usage: netstat [options]
Description: Displays network connections, routing tables, interface statistics, masquerade connections, and multicast memberships. For example, netstat -tuln shows all listening ports and their corresponding services. This command is essential for monitoring network traffic and identifying active connections.
36. ss (Another Utility to Investigate Sockets)
Usage: ss [options]
Description: A faster and more efficient alternative to netstat, ss provides detailed information about socket connections, including TCP, UDP, and raw sockets. For example, ss -tuln displays all listening sockets, similar to netstat -tuln. This command is particularly useful for diagnosing network issues.
37. traceroute (Print the Route Packets Take to a Network Host)
Usage: traceroute [destination]
Description: Traces the path packets take from your server to a specified destination, showing each hop along the way. For example, traceroute google.com shows the route taken to reach Google’s servers. This command helps identify where delays or failures occur in the network.
38. nslookup (Query Internet Name Servers Interactively)
Usage: nslookup [domain]
Description: Queries DNS servers to obtain domain name or IP address mapping. For example, nslookup example.com retrieves the IP address associated with “example.com”. This command is useful for troubleshooting DNS issues.
39. dig (DNS Lookup Utility)
Usage: dig [options] [domain]
Description: Performs detailed DNS queries, providing more comprehensive output than nslookup. For example, dig example.com retrieves the DNS records for “example.com”. The +short option simplifies the output to just the resolved IP address, making dig a versatile tool for DNS diagnostics.
40. scp (Secure Copy)
Usage: scp [options] [source] [destination]
Description: Securely copies files and directories between hosts over an SSH connection. For example, scp file.txt user@remote:/path/ copies “file.txt” to the specified directory on a remote server. This command is vital for transferring files securely between servers.
41. ssh (OpenSSH SSH Client)
Usage: ssh [options] [user@hostname]
Description: Connects to a remote server using the SSH protocol, allowing for secure command-line access. For example, ssh user@remote-server.com establishes a secure connection to “remote-server.com”. SSH is fundamental for remote server management.
42. wget (Non-interactive Network Downloader)
Usage: wget [options] [URL]
Description: Downloads files from the web via HTTP, HTTPS, or FTP. For example, wget http://example.com/file.zip downloads “file.zip” from the specified URL. wget is particularly useful for automated scripts and downloading files without user intervention.
43. curl (Transfer Data From or To a Server)
Usage: curl [options] [URL]
Description: Transfers data from or to a server using a variety of protocols, including HTTP, HTTPS, FTP, and more. For example, curl -O http://example.com/file.zip downloads “file.zip” like wget, but curl also supports complex operations like POST requests and authentication, making it a powerful tool for web interactions.
44. nmap (Network Exploration Tool and Security/Port Scanner)
Usage: nmap [options] [target]
Description: Scans networks for open ports, running services, and vulnerabilities. For example, nmap -sP 192.168.1.0/24 performs a ping scan to discover live hosts on the network. nmap is an essential tool for network security audits and exploration.
45. tcpdump (Command-line Packet Analyzer)
Usage: tcpdump [options]
Description: Captures and analyzes network packets in real-time. For example, tcpdump -i eth0 captures all packets on the eth0 interface. This command is invaluable for troubleshooting network issues and monitoring traffic at a granular level.
Network management commands are critical for maintaining the health and security of your Linux server’s network connections. These tools allow you to configure interfaces, monitor traffic, troubleshoot connectivity issues, and secure your network against potential threats.

User and Permission Management
User and permission management commands are fundamental for controlling access to your Linux server. These commands allow you to create, modify, and manage user accounts, groups, and permissions, ensuring that only authorized users can access specific files and perform certain actions.

46. useradd / adduser (Create a New User)
Usage: useradd [options] username / adduser [username]
Description: useradd and adduser are used to create new user accounts. While useradd is more basic, adduser is a friendlier, interactive script that prompts you to enter user details like password, home directory, and shell. For example, useradd john creates a new user named “john”.
47. usermod (Modify a User Account)
Usage: usermod [options] username
Description: Modifies existing user accounts, such as changing the username, user ID, group ID, home directory, or shell. For example, usermod -l newname oldname changes the username from “oldname” to “newname”.
48. userdel (Delete a User Account)
Usage: userdel [options] username
Description: Deletes a user account from the system. The -r option removes the user’s home directory and mail spool as well. For example, userdel -r john deletes the user “john” and their home directory.
49. passwd (Change User Password)
Usage: passwd [username]
Description: Changes the password of a user account. Without any options, passwd changes the password of the current user. For example, passwd john changes the password for the user “john”. This command is also used to manage account expiration dates and lock or unlock user accounts.
50. groups (Show User Groups)
Usage: groups [username]
Description: Displays the groups that a user belongs to. For example, groups john shows all groups that “john” is a member of. This command is useful for verifying group memberships.
51. sudo (Execute a Command as Another User)
Usage: sudo [command]
Description: Allows a permitted user to execute a command as the superuser or another user, as specified by the security policy. For example, sudo apt-get update runs the package update command with superuser privileges. sudo is essential for performing administrative tasks without logging in as the root user.
52. chown (Change File Owner and Group)
Usage: chown [owner][:group] [file or directory]
Description: Changes the ownership of a file or directory. For example, chown john:admin file.txt changes the owner of “file.txt” to “john” and its group to “admin”. This command is crucial for managing file access and ownership in a multi-user environment.
53. chmod (Change File Modes or Access Permissions)
Usage: chmod [permissions] [file or directory]
Description: Changes the access permissions of files or directories. Permissions can be set using symbolic (e.g., chmod u+x file) or numeric (e.g., chmod 755 file) modes. For instance, chmod 644 file.txt sets read and write permissions for the owner and read-only for others.
54. umask (Set Default File Permissions)
Usage: umask [mask]
Description: Sets the default permissions for newly created files and directories. The umask value determines which permission bits will not be set on newly created files. For example, umask 022 results in new files having permissions of 755 (readable and executable by everyone, writable only by the owner).
55. id (Print User and Group Information)
Usage: id [username]
Description: Displays the user ID (UID), group ID (GID), and group memberships for a user. For example, id john shows the UID, GID, and all group memberships for “john”. This command is useful for verifying a user’s identity and permissions.
56. su (Substitute User Identity)
Usage: su [options] [username]
Description: Switches to another user account, allowing you to execute commands with that user’s privileges. For example, su – john switches to the “john” account with the user’s environment. If no username is specified, it defaults to the superuser (root).
57. gpasswd (Administer /etc/group and /etc/gshadow)
Usage: gpasswd [options] [group]
Description: Manages /etc/group and /etc/gshadow, allowing you to set passwords, add users to groups, and remove users from groups. For example, gpasswd -a john admin adds “john” to the “admin” group. This command is useful for managing group memberships and security.
58. passwd -l (Lock a User Account)
Usage: passwd -l [username]
Description: Locks a user account, preventing them from logging in. For example, passwd -l john locks the account “john”. This is useful for temporarily disabling an account without deleting it.
59. passwd -u (Unlock a User Account)
Usage: passwd -u [username]
Description: Unlocks a previously locked user account, allowing them to log in again. For example, passwd -u john unlocks the “john” account.
60. who (Show Who is Logged On)
Usage: who
Description: Displays information about all users currently logged into the system, including their terminal, login time, and source IP. This command is helpful for monitoring user activity on the server.
61. w (Show Who is Logged On and What They Are Doing)
Usage: w
Description: Provides more detailed information than who, showing not only who is logged in but also what processes they are running. For example, it shows how long the user has been idle and their CPU usage. This command is useful for identifying users who are consuming system resources.
62. last (Show Listing of Last Logged in Users)
Usage: last [options]
Description: Displays a list of the last logged-in users, including the time they logged in and out, and their IP address. This command is useful for auditing and tracking user logins.
User and permission management commands are essential for maintaining the security and integrity of your Linux server. These commands help you control who can access the server, what they can do, and ensure that permissions are correctly configured to protect sensitive data.

Request A Free 15-day Trial of Zentyal Server

Package Management
Package management commands are essential for installing, updating, and managing software on a Linux server. Different Linux distributions have their own package management systems, and these commands help you keep your server’s software up-to-date and secure.

63. apt-get / apt (Debian/Ubuntu Package Handling Utility)
Usage: apt-get [options] [command] / apt [options] [command]
Description: apt-get and apt are the primary package management tools for Debian-based systems like Ubuntu. They are used for installing, updating, upgrading, and removing packages. Common commands include:
apt-get update: Updates the package list.
apt-get upgrade: Upgrades all installed packages to their latest versions.
apt-get install [package]: Installs a specified package.
apt-get remove [package]: Removes a specified package.
apt is a more user-friendly command that combines functions of apt-get, apt-cache, and dpkg.
64. yum / dnf (CentOS/Fedora Package Manager)
Usage: yum [options] [command] / dnf [options] [command]
Description: yum (Yellowdog Updater, Modified) and dnf (Dandified YUM) are the package management tools for RPM-based distributions like CentOS and Fedora. They are used for similar tasks as apt-get in Debian-based systems. Common commands include:
yum update / dnf update: Updates all installed packages.
yum install [package] / dnf install [package]: Installs a specified package.
yum remove [package] / dnf remove [package]: Removes a specified package.
dnf is the next-generation version of yum, offering better performance and a cleaner command syntax.
65. rpm (RPM Package Manager)
Usage: rpm [options] [command]
Description: The low-level RPM Package Manager is used to install, query, verify, update, and remove packages on RPM-based systems like Red Hat, CentOS, and Fedora. Common commands include:
rpm -i [package.rpm]: Installs a package.
rpm -e [package]: Removes a package.
rpm -qa: Lists all installed packages.
rpm -qf [file]: Identifies which package a file belongs to.
66. dpkg (Debian Package Manager)
Usage: dpkg [options] [command]
Description: dpkg is the low-level package manager for Debian-based systems, used to install, remove, and provide information about .deb packages. For example:
dpkg -i [package.deb]: Installs a .deb package.
dpkg -r [package]: Removes an installed package.
dpkg -l: Lists all installed packages.
dpkg –configure -a: Reconfigures unpacked but unconfigured packages.
67. pacman (Arch Linux Package Manager)
Usage: pacman [options] [command]
Description: pacman is the package manager for Arch Linux, used to manage packages from the official repositories and user-contributed packages from the Arch User Repository (AUR). Common commands include:
pacman -Syu: Updates the system by synchronizing the package database and upgrading all packages.
pacman -S [package]: Installs a specified package.
pacman -R [package]: Removes a specified package.
pacman -Ss [package]: Searches for a package in the repositories.
68. snap (Snap Package Manager)
Usage: snap [options] [command]
Description: snap is a package management system that allows for installing and managing “snaps,” which are containerized software packages that work across many Linux distributions. Common commands include:
snap install [package]: Installs a snap package.
snap remove [package]: Removes a snap package.
snap refresh: Updates all installed snap packages.
snap list: Lists all installed snap packages.
69. flatpak (Flatpak Package Manager)
Usage: flatpak [options] [command]
Description: flatpak is a package management system for building, distributing, and running sandboxed desktop applications on Linux. Common commands include:
flatpak install [remote] [package]: Installs a flatpak application.
flatpak remove [package]: Removes a flatpak application.
flatpak update: Updates installed flatpak applications.
flatpak list: Lists installed flatpak applications.
70. apt-cache (Debian/Ubuntu Package Query Tool)
Usage: apt-cache [command]
Description: Queries information about packages in the APT package database. For example, apt-cache search [package] searches for packages in the repositories, and apt-cache show [package] displays detailed information about a package.
71. brew (Linuxbrew Package Manager)
Usage: brew [command]
Description: brew is a package manager originally developed for macOS, but it can also be used on Linux via Linuxbrew. It’s used for installing software not included in the distribution’s official repositories. Common commands include:
brew install [package]: Installs a specified package.
brew remove [package]: Removes a specified package.
brew update: Updates the list of available packages.
brew upgrade: Upgrades installed packages.
Package management commands are vital for maintaining a secure and up-to-date Linux server. These tools allow you to install, update, and manage software packages, ensuring that your server has the necessary software and security patches to operate efficiently.

Process Management
Process management commands are crucial for monitoring and controlling running processes on a Linux server. These commands help administrators manage system resources, terminate unresponsive processes, and ensure that the server operates smoothly.

72. ps (Report a Snapshot of Current Processes)
Usage: ps [options]
Description: Displays information about the currently running processes, including their PID (Process ID), TTY (terminal type), time, and command name. For example, ps aux shows all running processes with detailed information, and ps -ef provides a similar output in a different format.
73. top (Display Linux Tasks)
Usage: top
Description: Provides a real-time view of running processes, including CPU and memory usage. It allows you to monitor system performance and identify resource-intensive processes. top also allows you to kill processes directly from the interface by pressing k and entering the PID.
74. htop (Interactive Process Viewer)
Usage: htop
Description: Similar to top, but with an enhanced user interface that is more user-friendly and visually appealing. htop allows you to scroll through the process list horizontally and vertically, and provides color-coded information for easier reading.
75. kill (Terminate a Process by PID)
Usage: kill [options] [PID]
Description: Sends a signal to a process to terminate it. The most common signal is SIGKILL (9), which forcefully stops the process. For example, kill -9 1234 sends the SIGKILL signal to the process with PID 1234.
76. killall (Kill Processes by Name)
Usage: killall [options] [process name]
Description: Terminates all processes with the specified name. For example, killall firefox kills all instances of the “firefox” process. This command is useful for stopping multiple instances of a process without knowing their PIDs.
77. pkill (Send Signals to Processes by Name)
Usage: pkill [options] [process name]
Description: Sends a signal to processes based on name and other attributes. For example, pkill -9 sshd sends the SIGKILL signal to the “sshd” process. It’s similar to killall but offers more options for targeting specific processes.
78. nice (Run a Command with Modified Scheduling Priority)
Usage: nice [options] [command]
Description: Starts a command with a specified priority (niceness). Lower values indicate higher priority. For example, nice -n 10 command runs “command” with a lower priority, ensuring it doesn’t take too many resources away from more important processes.
79. renice (Alter the Priority of a Running Process)
Usage: renice [options] [new priority] [PID]
Description: Changes the priority of an already running process. For example, renice -n 10 1234 changes the priority of the process with PID 1234 to a lower priority. This command is useful for adjusting resource allocation on the fly.
80. bg (Resume a Suspended Job in the Background)
Usage: bg [job ID]
Description: Resumes a suspended job and runs it in the background. For example, if a job has been paused using Ctrl+Z, typing bg %1 resumes job number 1 in the background.
81. fg (Bring a Job to the Foreground)
Usage: fg [job ID]
Description: Brings a background job to the foreground. For example, fg %1 brings job number 1 to the foreground, allowing you to interact with it directly.
82. jobs (List Active Jobs)
Usage: jobs
Description: Lists all jobs running in the background or suspended in the current terminal session. Each job is assigned a unique job ID, which can be used with bg or fg.
83. strace (Trace System Calls and Signals)
Usage: strace [options] [command]
Description: Traces system calls and signals received by a process. For example, strace ls shows all system calls made by the ls command. This command is invaluable for debugging and understanding how a program interacts with the operating system.
84. lsof (List Open Files)
Usage: lsof [options]
Description: Lists all open files and the processes that opened them. For example, lsof -i :80 shows all processes using port 80. This command is essential for diagnosing issues related to file locks, network sockets, and more.
85. systemctl (Examine and Control the Systemd System and Service Manager)
Usage: systemctl [options] [command]
Description: Controls the systemd system and service manager, allowing you to start, stop, enable, disable, and check the status of services. For example, systemctl start nginx starts the Nginx service, and systemctl status nginx shows its current status.
86. service (Run a System V Init Script)
Usage: service [service name] [command]
Description: Manages services on systems that use System V init scripts. Common commands include start, stop, restart, and status. For example, service apache2 restart restarts the Apache service.
Process management commands are essential for maintaining control over the processes running on your Linux server. These commands help you monitor system performance, prioritize tasks, and terminate unresponsive processes, ensuring that your server operates efficiently and reliably.

Must Read: How to Choose the Best Linux Server Distro in 2024

Disk Management
Disk management commands are essential for managing and maintaining the storage devices on your Linux server. These commands allow you to create, format, mount, and manage partitions and file systems, as well as monitor disk usage and health.

87. fdisk (Partition Table Manipulator for Linux)
Usage: fdisk [device]
Description: A command-line utility for viewing and editing the partition table on a hard drive. For example, fdisk /dev/sda opens the partition table for the /dev/sda disk, allowing you to create, delete, and modify partitions. It’s a powerful tool for managing disk partitions.
88. parted (A Partition Editor)
Usage: parted [device]
Description: A more advanced partition editor that supports a wider range of partition types and sizes than fdisk. For example, parted /dev/sda allows you to manage partitions on the /dev/sda disk, including creating GPT partitions, resizing, and moving partitions.
89. mkfs (Build a Linux File System)
Usage: mkfs [options] [device]
Description: Creates a file system on a partition. For example, mkfs.ext4 /dev/sda1 formats the /dev/sda1 partition with the ext4 file system. This command is used when setting up new partitions or reformatting existing ones.
90. mount (Mount a File System)
Usage: mount [options] [device] [mount point]
Description: Attaches a file system to the system’s file tree. For example, mount /dev/sda1 /mnt mounts the /dev/sda1 partition to the /mnt directory, making it accessible. This command is essential for accessing and managing external drives and partitions.
91. umount (Unmount File Systems)
Usage: umount [options] [mount point]
Description: Detaches a file system from the system’s file tree. For example, umount /mnt unmounts the file system mounted at /mnt. It’s important to unmount file systems before removing physical drives to prevent data loss.
92. lsblk (List Information About Block Devices)
Usage: lsblk [options]
Description: Lists information about all available block devices, such as hard drives and partitions, including their size, type, and mount points. For example, lsblk displays a tree view of all block devices, making it easy to see the structure of your disks and partitions.
93. blkid (Locate/Print Block Device Attributes)
Usage: blkid [options] [device]
Description: Prints the UUID and other attributes of a block device. For example, blkid /dev/sda1 returns the UUID and file system type of the /dev/sda1 partition. This command is useful for identifying devices and configuring fstab for persistent mounts.
94. df (Report File System Disk Space Usage)
Usage: df [options]
Description: Displays the amount of disk space used and available on all mounted file systems. The -h option provides a human-readable format, showing sizes in KB, MB, or GB. This command is essential for monitoring disk usage and ensuring sufficient free space.
95. du (Estimate File Space Usage)
Usage: du [options] [directory or file]
Description: Summarizes disk usage of files and directories. For example, du -sh /var/log shows the total size of the /var/log directory in a human-readable format. This command is useful for identifying large files and directories that may be consuming excessive disk space.
96. fsck (File System Consistency Check and Repair)
Usage: fsck [options] [file system]
Description: Checks and repairs file system inconsistencies. For example, fsck /dev/sda1 checks and repairs the file system on the /dev/sda1 partition. This command is crucial for maintaining the health of your file systems and preventing data corruption.
97. tune2fs (Adjust Tunable File System Parameters on ext2/ext3/ext4 File Systems)
Usage: tune2fs [options] [device]
Description: Modifies parameters of ext2, ext3, or ext4 file systems. For example, tune2fs -c 20 /dev/sda1 sets the maximum number of mounts before a file system check is forced. This command allows you to optimize file system performance and behavior.
98. swapoff (Disable Swap Space)
Usage: swapoff [device]
Description: Disables the specified swap space, making it unavailable for use. For example, swapoff /dev/sda2 disables the swap space on the /dev/sda2 partition. This command is often used before resizing or removing a swap partition.
99. swapon (Enable Swap Space)
Usage: swapon [device]
Description: Enables the specified swap space, making it available for use. For example, swapon /dev/sda2 enables the swap space on the /dev/sda2 partition. Managing swap space is important for system performance, especially on systems with limited physical memory.
100. mount -o remount (Remount a File System with Different Options)
Usage: mount -o remount,[options] [mount point]
Description: Remounts a file system with new mount options without unmounting it. For example, mount -o remount,rw /mnt remounts the file system at /mnt with read-write permissions. This is useful for changing mount options on-the-fly.
Disk management commands are critical for maintaining the health and efficiency of your Linux server’s storage systems. These tools allow you to manage partitions, file systems, and disk usage effectively, ensuring that your server has the storage resources it needs to operate smoothly.

Conclusion
Mastering Linux server commands is essential for anyone responsible for managing and maintaining a Linux server. From basic file operations to advanced disk management and network configuration, these 100 commands provide a comprehensive toolkit for effective server administration. By understanding and utilizing these commands, you can optimize server performance, enhance security, and ensure that your system runs smoothly and efficiently.

Whether you are a seasoned sysadmin or just starting your journey in Linux server management, this guide serves as a valuable resource. It empowers you with the knowledge and skills needed to tackle the diverse challenges that arise in a Linux environment. As you continue to explore and apply these commands, you’ll find that the command line becomes an indispensable ally in your server management tasks.

Remember, while this guide covers a wide array of commands, the Linux ecosystem is vast and constantly evolving. Stay curious, keep learning, and don’t hesitate to explore new commands and tools that can further enhance your server management capabilities.