### Step 1: What Is Caido?

Caido is a web security auditing toolkit that acts as an interception proxy between your browser and your target web applications. It allows you to inspect, manipulate, and replay HTTP/S and WebSocket traffic in real-time, making it easier to discover and exploit security vulnerabilities. Sounds similar to Burp Suite or ZAP, isn't it?

**Why people choose Caido:**

- Modern and lightweight
- Easier for beginners
- Ideal for manual testing and request manipulation
- Actively developed and responsive to community feedback

### Step 2: Installing Caido

Getting Caido up and running is straightforward.

Download the latest installer from Caido's official website or GitHub releases. Install .deb via terminal:

```bash
sudo dpkg -i caido-desktop-v0.55.3-linux-x86_64.deb
```
You can also get Caido from the Kali repository:
sudo apt install caido
![Caido Download](/writeups/images/caido1.png)

After downloading, unpack as shown below:

![Unpacking Caido](/writeups/images/caido2.png)

Launch Caido and start the instance by clicking on the Start button

![Start Instance](/writeups/images/caido3.png)

Then launch:
caido
You will be greeted by a screen like below.

![Caido Home](/writeups/images/caido4.png)

### Step 3: Navigation

On the left-hand side of Caido is a navigation menu that contains the different feature interfaces.

![Navigation](/writeups/images/caido5.png)

### Step 4: Using Caido

The Intercept, Replay, and Automate features allow you to view, modify, and control web traffic.

Intercept

With Caido running and proxy enabled, clicking the >> Forwarding button will switch Caido to Queuing mode. You can intercept requests before they are sent to the server or intercept responses.

![Intercept Mode](/writeups/images/caido6.png)

As traffic accumulates, you can view all intercepted requests and responses.

Replay

By clicking on a request, you can send it to Replay using `Ctrl + R`, or by right-clicking and selecting Send to Replay.

![Send to Replay](/writeups/images/caido7.png)

Here, you can manipulate requests and view server responses.

![Replay Editor](/writeups/images/caido8.png)

### Step 5: Caido vs Burp Suite

![Caido vs Burp](/writeups/images/caido9.png)

Project Management

Caido's built-in project management helps keep your work organized.

![Project Management](/writeups/images/caido10.png)

Intuitive Filtering

With HTTPQL, you can easily search and filter requests.

![HTTPQL Filtering](/writeups/images/caido11.png)

Built for Speed

Built from the ground up in Rust to deliver fast experience with low memory usage.

![Performance](/writeups/images/caido12.png)

### Summary

At this point, you might think Caido doesn't offer anything significantly different from Burp Suite. However, I highly recommend installing Caido and trying it out yourself. It might just become your next go-to tool for web app hacking.

If you want to start learning web hacking, check out our Web App Hacking course.

