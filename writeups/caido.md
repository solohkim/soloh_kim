### Step 1: What Is Caido?
Caido is a web security auditing toolkit that acts as an interception proxy between your browser (or other HTTP client) and your target web applications. It allows you to inspect, manipulate, and replay HTTP/S and WebSocket traffic in real-time, making it easier to discover and exploit security vulnerabilities. Sounds similarly like Burp Suite or ZAP, isn’t it? Why people choose Caido:

```bash
       Modern and lightweight
       Easier for beginners
       Ideal for manual testing and request manipulation
       Actively developed and responsive to community feedback
       ```

### Step 2: Installing Caido
Getting Caido up and running is straightforward:

Download the latest installer or package for your OS from Caido’s official website or GitHub releases. Install .deb file via terminal: kali> sudo dpkg -i caido-desktop-v[version].deb

You can also get Caido from the Kali repository by entering:

kali > sudo apt install caido


![scan](/writeups/images/caido1.png)

After downloading, use the following command to unpack as shown below

![scan](/writeups/images/caido2.png)


Launch Caido and start the instance by clicking on the Start button

![scan](/writeups/images/caido3.png)

kali > caido After that, you will be greeted by a screen like below.

![scan](/writeups/images/caido4.png)


### Step 3: Navigation

On the left-hand side of Caido is a navigation menu that contains the different feature interfaces. Clicking on a listed feature will present its own page.

![scan](/writeups/images/caido5.png)


### Step 4: Using Caido
The Intercept, Replay, and Automate feature interfaces allow you to view, modify, and control web traffic.

Intercept
With Caido running and the proxy settings enabled, clicking the >> Forwarding button will switch Caido to || Queuing mode. In this mode, you can intercept requests before they are sent to the server or intercept responses before they are sent to your browser.

From the Intercept interface, you can choose to intercept requests, responses, or both by clicking the corresponding buttons. A pause icon will appear when intercept is enabled, and two right-facing carets will appear when it is disabled.

![scan](/writeups/images/caido6.png)


As web traffic accumulates, you can view all intercepted requests and responses in the Intercept traffic tables.

### Replay
By clicking on a request, you can send it to Replay using the keyboard shortcut Ctrl + R, or by right-cl! licking and selecting Send to Replay from the context menu.

![scan](/writeups/images/caido7.png)



Here, we can manipulate our requests and view the responses from the server.

![scan](/writeups/images/caido8.png)


### step 5: Caido vs Burp Suite
Up to this point, we’ve covered the basic functionality of Caido, similar to what’s available in tools like Burp Suite. Now, let’s look at some features that make it unique.


![scan](/writeups/images/caido9.png)


### Project Management
Caido’s built-in project management system helps keep your work organized and makes managing targets effortless. You can easily switch between different targets as needed.


![scan](/writeups/images/caido10.png)

### Intuitive Filtering
With HTTPQL, you can easily search and filter requests using a simple, user-friendly query language.

![scan](/writeups/images/caido11.png)


### Built for Speed
While Burp Suite struggles with resource efficiency, Caido is built from the ground up in Rust to deliver a fast experience with low memory usage and unparalleled performance.

![scan](/writeups/images/caido12.png)


### Summary
At this point, you might think that Caido doesn’t offer anything significantly different from Burp Suite. However, I highly recommend installing Caido and trying it out for yourself—experiment with it. This article only scratches the surface of what Caido has to offer. It might just become your next go-to tool for web app hacking.

If you want to start learning web hacking, check out our Web App Hacking course — it covers everything you need to know to begin.