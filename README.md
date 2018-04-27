DSR IPTV Server
===============

Overview:

dsrip exposes an DSR as an IPTV source when can then be used by other applications such as tvheadend, kodi, vlc, etc.

How to use:
for now you need udpxy in order to convert the multicast stream coming out of the DSR's GigE interface to a HTTP stream.

Configuration:
[server]
ListeningAddress = 0.0.0.0
ListeningPort = 80

[dsr0]
Comment = DSR-6000
SnmpAddress = 192.168.1.100
StreamUrl = http://localhost:4022/udp/239.1.1.1:6100

Examples:
  $ ./udpxy -v -a enp2s0f0 -p 4022 -m enp2s0f1
  $ sudo ./dsrip.py

Commands:
* status:
    http://<ip>:<port>/status/<instance>

* tune:
    http://<ip>:<port>/tune/<instance>?<parameters>
    
* tune & stream:
    http://<ip>:<port>/stream/<instance>?<parameters>
