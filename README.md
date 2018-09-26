MNemu 
========

## What is MNemu? ##
MNemu is an open-source application developed to provide a simple, lightweight
network emulation tool for testing and developing web, mobile, and standalone
applications under various networking conditions. It was designed as a easy to 
use interface to harness the power of the Linux Kernel **tc netem** commands across 
multiple clients in real-time.

#### Current State ####
Currently Mnemu is under very active development. While the core abilities that
MNemu was originally designed for are functional, bugs and changes should be 
expected. A good portion of the codebase will undergo 'cleanup' and polish as 
we approach a v1.0<br><br>


**MNemu Web App**
![MNemu Mainscreen](https://corefracture.com/wp-content/uploads/2018/09/mnemu.png)



## Current Features ##


* **Simplistic TC Netem Configuration**<br>
Provides a simple web-based interface for creating tc netem configurations on a 
per IP basis.

* **Per IP Inbound and Outbound Traffic Manipulation**<br>
MNemu allows for isolating network emulation rules to be set per IP and for the 
inbound and outbound traffic of that IP. 

* **(Webapp) - Device IP, Favorite IPs, and Ignored IP Sections**<br>
The web app interface shows the IP of the connecting device to allow users to 
simply visit the page with the device they wish to manipulate network conditions 
on. Users can also ignore certain IPs and set favorite IPs.

* **(Webapp) - Presets**<br>
MNemus web app allows for quickly setting various 'preset' network conditions on 
the inbound and outbound traffic with a simple dropdown selection

* **(Webapp) - Bandwidth, Ping, Loss, Duplication, and Corruption NetEm Settings**<br>
The current version of the web app allows users to set the common netem rules for 
the inbound and outbound traffic of any IP routing through the system

* **REST API**<br>
While the API will undergo some organization changes, it is a fully functional
interface to the MNemu applications abilities

## Features Coming Very Soon ##
* **Scripting**<br>
Soon MNemu will allow users to create 'scripts' to change the network emulation
conditions. Scripts will initially allow users to set various conditions at certain
times, for certain intervals of time, or at random points. 

* **Remaining Netem Settings**<br>
Adding the 'correlation' settings for all the available Netem settings.

* **Preventing Network Conditioning To and From MNemu Server**<br>
Currently users can still 'kill' their connections to completely by settings
an extremely low bandwidth limit or severe packet loss. This also prevents
the users from reaching the MNemu web app to fix their connections. 

* **Simple Monitoring**<br>
Simple traffic statistics for IPs being actively conditioned.


## More Planned Features (In The Future) ##
* **Realtime Packet Capture**<br>
Adding the ability to perform a tcpdump on an active IP being conditioned by
the MNemu server.

* **Possible IPv6 Support**<br>
Support for IPv6 networks


