DSR IPTV Server
===============

Overview:

dsrip exposes an DSR as an IPTV source when can then be used by other applications such as tvheadend, kodi, vlc, etc.


How to use:

First, you need to use 'udpxy' as a proxy between the DSR's multicast stream and the HTTP stream we'll redirect to the calling application.

Second, edit the dsrip.ini file to reflect your DSR instances and addresses.

Run udpxy and dsrip...

i.e.:

  $ ./udpxy -v -a enp2s0f0 -p 4022 -m enp2s0f1
  $ sudo ./dsrip.py

Status url:

  http://<ip>:<port>/status/<instance>

Tuning url:

  http://<ip>:<port>/tune/<instance>?<parameters>

Streaming url:

  http://<ip>:<port>/stream/<instance>?<parameters>


The following is a list of tuning/streaming parameters:

+-------------+--------------+---------------------------+--------------------+
| name        | attribute    | value                     | examples           |
+-------------+--------------+---------------------------+--------------------+
| RF Port     | port         | integer between 1 and 8   | port=1             |
| Frequncy    | freq         | float freq in MHz         | freq=4080          |
| Modulation  | modulation   | dcii, dvbs, turbo, dvbs2  | modulation=dvbs2   |
| Symbol Rate | sr           | fload in kSymb/s          | sr=31250           |
| FEC inner   | fec          | depends on modulation     | fec=34             |
| Service ID  | sid          | service id to stream      | sid=1              |
+-------------+--------------+---------------------------+--------------------+

Example:
  http://tvheadend/stream/dsr0?port=1&freq=3740&modulation=dvbs2&sr=31250&fec=34&sid=2

In my setup, port 1 is connected to horizontal and port 2 is connected to vertical.
