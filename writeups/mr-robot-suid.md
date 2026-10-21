# Mr Robot — SUID nmap to Root
**Platform:** TryHackMe | **Difficulty:** Easy

## Recon
nmap -sV target...

## PrivEsc
Found SUID nmap: `nmap --interactive -> !sh`

## Mitigation
Remove SUID, use capabilities.

> Flag redacted — methodology > flags