***CORRUPTION WRITEUP----*** from skillbit


QZ:

Oh no! I tried downloading a picture for my upcoming conference talk but it won't open! Can you see if you can fix it and open it?

You can download it here: corrupted.png.

![png](/writeups/images/corruption1.png)

From the web we can see it's already broken

![web](/writeups/images/corrupted1.png)

so i downloaded the corrupted.png file 
using 
```bash
wget $BASH_COMMAND
```
![wget](/writeups/images/corruption2.png)


I listed the contents
and discoved the details using info command 

![info](/writeups/images/corruption3.png)


Using pdfdetach, i checked if we had any embeddedfiles
```bash
                                                                                                                                                            
┌──(solohkim㉿kali)-[~/CyberSec/skillbit/LC]
└─$ pdfdetach -list corrupted.png
0 embedded files

```

Upon using a web fuzzer, i saw something here

![caido](/writeups/images/corruption4.png)

After discovering this i had to extract the pdf items using this command:

```bash
pdfimages -all corrupted.png extracted
```
![extract](/writeups/images/corruption5.png)

After extracting i realized something interesting:


![pdfextr](/writeups/images/corruption6.png)

Then i opened the extracted-000.png file
using this command
```bash
xdg-open extracted-000.png
```

And boom here is our flag:


![flag](/writeups/images/corruption7.png)

```bash
Flag: MetaCTF{0p3rating_$ystems_1ike_ext3nsions}
```


