# DSRIP Server

The goal of this program to is expose a Motorola DSR-6000 as an IPTV source using a SAT>IP style URL.

## Getting Started

First, you need to use 'udpxy' as a proxy between the DSR's multicast stream and the HTTP stream we'll redirect to the calling application.

### Prerequisites

Python 2.7+ and following python packages:

* ConfigParser
* SimpleHTTPServer 
* BaseHTTPRequestHandler
* HTTPServer
* SocketServer
* urlparse
* netsnmp
* requests
* ipaddress
* socket
* struct
* sys
* time
* os

### Configuration

Edit dsrip.ini to relect your DSR settings.

Example:
```
[server]
ListeningAddress = 0.0.0.0
ListeningPort = 80

[dsr0]
Comment = DSR-6000
SnmpAddress = 192.168.1.100
StreamUrl = udp://@:6100 # unicast
Source1_LOF = 5150
Source1_HPort = 6
Source1_VPort = 7

[dsr1]
Comment = DSR-6000
SnmpAddress = 192.168.1.101
StreamUrl = udp://@239.1.1.1:6100 # unicast
Source1_LOF = 5150
Source1_HPort = 6
Source1_VPort = 7
```

### Running

  $ python dsrip.py

### Testing

Status url:

  http://<ip>:<port>/status/<instance>

Tuning url:

  http://<ip>:<port>/tune/<instance>?<parameters>

Streaming url:

  http://<ip>:<port>/stream/<instance>?<parameters>


The following is a list of tuning/streaming parameters:

| name         | attribute    | value                     | examples           |
|--------------|--------------|---------------------------|--------------------|
| RF Port      | port         | integer between 1 and 8   | port=1             |
| Polarization | pol          | v, h                      | pol=v              |
| Frequncy     | freq         | float freq in MHz         | freq=4080          |
| Modulation   | modulation   | dcii, dvbs, turbo, dvbs2  | modulation=dvbs2   |
| Symbol Rate  | sr           | fload in kSymb/s          | sr=31250           |
| FEC inner    | fec          | depends on modulation     | fec=34             |
| Service ID   | sid          | service id to stream      | sid=1              |

Example:
```
  http://localhost/stream/?fe=1&pol=v&freq=4020&modulation=dvbs2&sr=31250&fec=34&sid=3
```
