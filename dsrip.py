#!/usr/bin/env python

import configparser
import SimpleHTTPServer 
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import netsnmp
import requests
import time
import os

netsnmp.verbose = 1

config = configparser.ConfigParser()

def tune_dcii(session, port, freq, sr, fec, split):
    freq_plan = 1 # default to l-freq

    if freq > 0 and freq < 25:
        freq_plan = 0

    fmt = 0

    if sr == 29270:
        if fec == 511:
            fmt = fmt + 0
        elif fec == 12:
            fmt = fmt + 1
        elif fec == 35:
            fmt = fmt + 2
        elif fec == 23:
            fmt = fmt + 3
        elif fec == 34:
            fmt = fmt + 4
        elif fec == 45:
            fmt = fmt + 5
        elif fec == 56:
            fmt = fmt + 6
        elif fec == 78:
            fmt = fmt + 7
        else:
            print "Invalid FEC for DCII!"
    elif sr == 19510:
        fmt = 16
        if fec == 511:
            fmt = fmt + 0
        elif fec == 12:
            fmt = fmt + 1
        elif fec == 35:
            fmt = fmt + 2
        elif fec == 23:
            fmt = fmt + 3
        elif fec == 34:
            fmt = fmt + 4
        elif fec == 45:
            fmt = fmt + 5
        elif fec == 56:
            fmt = fmt + 6
        elif fec == 78:
            fmt = fmt + 7
        else:
            print "Invalid FEC for DCII!"
    else:
        if sr == 14630:
            fmt = 32
        elif sr == 11710:
            fmt = 39
        elif sr == 9760:
            fmt = 46
        elif sr == 7320:
            fmt = 53
        elif sr == 4880:
            fmt = 60
        elif sr == 3250:
            fmt = 67
        else:
            print "Invalid SR for DCII!"

        if fec == 12:
            fmt = fmt + 0
        elif fec == 35:
            fmt = fmt + 1
        elif fec == 23:
            fmt = fmt + 2
        elif fec == 34:
            fmt = fmt + 3
        elif fec == 45:
            fmt = fmt + 4
        elif fec == 56:
            fmt = fmt + 5
        elif fec == 78:
            fmt = fmt + 6
        else:
            print "Invalid FEC for DCII!"

    vars = netsnmp.VarList(
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.1.0', port, 'INTEGER'),             # Port
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.2.0', freq_plan, 'INTEGER'),        # Frequency plan
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.9.0', 0, 'INTEGER'),                # Mode
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.7.0', split, 'INTEGER'),            # Format: 0=Split, 1=Combined
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.8.0', fmt, 'INTEGER'),              # SR+FEC
            )

    print 'Configuring port, freq_plan, mode, format and sr+fec...'
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    if freq_plan == 0:
        vars = netsnmp.VarList(
                netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.3.0', int(freq), 'INTEGER'),     # xpndr
                )
    else:
        vars = netsnmp.VarList(
                netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.4.0', int(5150 - freq), 'INTEGER'),     # l-freq
                )

    print 'Configuring xpndr/l-freq...'
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    return

def tune_dvbs(session, port, freq, sr, fec):
    freq_plan = 1 # default to l-freq

    if fec == 12:
        fec = 0
    elif fec == 23:
        fec = 1
    elif fec == 34:
        fec = 2
    elif fec == 56:
        fec = 3
    elif fec == 78:
        fec = 4
    else:
        print "Invalid FEC for DVBS!"

    if freq > 0 and freq < 25:
        freq_plan = 0

    vars = netsnmp.VarList(
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.1.0', port, 'INTEGER'),             # Port
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.2.0', freq_plan, 'INTEGER'),        # Frequency plan
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.9.0', 1, 'INTEGER'),                # Mode
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.5.0', int(sr) * 1000, 'INTEGER'),   # SR
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.6.0', fec, 'INTEGER'),              # FEC
            )

    print 'Configuring port, freq_plan, mode, sr and fec...'
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    if freq_plan == 0:
        vars = netsnmp.VarList(
                netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.3.0', int(freq), 'INTEGER'),     # xpndr
                )
    else:
        vars = netsnmp.VarList(
                netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.4.0', int(5150 - freq), 'INTEGER'),     # l-freq
                )

    print 'Configuring xpndr/l-freq...'
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    return

def tune_turbo(session, port, freq, sr, fec):
    freq_plan = 1 # default to l-freq


    if fec == 1.92:
        fec = 0
    elif fec == 2.05:
        fec = 1
    elif fec == 2.11:
        fec = 2
    elif fec == 2.19:
        fec = 3
    elif fec == 2.30:
        fec = 4
    elif fec == 2.40:
        fec = 5
    else:
        print "Invalid FEC for Turbo!"

    if freq > 0 and freq < 25:
        freq_plan = 0

    vars = netsnmp.VarList(
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.1.0', port, 'INTEGER'),                 # Port
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.2.0', freq_plan, 'INTEGER'),            # Frequency plan
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.9.0', 2, 'INTEGER'),                    # Mode
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.12.0', int(sr) * 1000, 'INTEGER'),      # SR
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.11.0', fec, 'INTEGER'),                 # FEC
            )
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    if freq_plan == 0:
        vars = netsnmp.VarList(
                netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.3.0', int(freq), 'INTEGER'),     # xpndr
                )
    else:
        vars = netsnmp.VarList(
                netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.4.0', int(5150 - freq), 'INTEGER'),     # l-freq
                )

    print 'Configuring xpndr/l-freq...'
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    return

def tune_dvbs2(session, port, freq, sr, fec):
    freq_plan = 1 # default to l-freq

    if fec == 35:
        fec = 0
    elif fec == 23:
        fec = 1
    elif fec == 34:
        fec = 2
    elif fec == 56:
        fec = 3
    elif fec == 89:
        fec = 4
    elif fec == 910:
        fec = 5
    else:
        print "Invalid FEC for DVBS2!"

    if freq > 0 and freq < 25:
        freq_plan = 0

    vars = netsnmp.VarList(
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.1.0', port, 'INTEGER'),             # Port
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.2.0', freq_plan, 'INTEGER'),        # Frequency plan
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.9.0', 4, 'INTEGER'),                # Mode
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.12.0', int(sr) * 1000, 'INTEGER'),  # SR
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.13.0', fec, 'INTEGER'),             # FEC
            )

    print 'Configuring port, freq_plan, mode, sr and fec...'
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    if freq_plan == 0:
        vars = netsnmp.VarList(
                netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.3.0', int(freq), 'INTEGER'),     # xpndr
                )
    else:
        vars = netsnmp.VarList(
                netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.2.2.4.0', int(5150 - freq), 'INTEGER'),     # l-freq
                )

    print 'Configuring xpndr/l-freq...'
    for var in vars:
       print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    return

def tune(instance, session, qs):
    # Signal source
    if 'src' in qs:
        src = int(qs['src'][0])
    else:
        src = 1

    # Polarisation
    if 'pol' in qs:
        key = "Source" + str(src) + "_" + qs['pol'][0].upper() + "Port"
        port = int(instance[key])
    elif 'port' in qs:
        port = int(qs['port'][0])
    else:
        raise ('missing pol or port parameter')

    # Frequency
    if 'freq' in qs:
        freq = float(qs['freq'][0])
    else:
        raise ('missing freq parameter')

    # Modulation
    if 'modulation' in qs:
        modulation = qs['modulation'][0]
    else:
        raise ('missing modulation parameter')

    # Symbol rate
    if 'sr' in qs:
        sr = float(qs['sr'][0])
    else:
        raise ('missing sr parameter')

    # Forward error correction
    if 'fec' in qs:
        fec = int(qs['fec'][0])
    else:
        raise ('missing fec parameter')

    if modulation == 'dcii-auto':
        tune_dcii_auto(session, port, freq)
    elif modulation == 'dcii':
        if 'split' in qs:
            split = int(qs['split'][0])
        else:
            split = 0
        tune_dcii(session, port, freq, sr, fec, split)
    elif modulation == 'dvbs':
        tune_dvbs(session, port, freq, sr, fec)
    elif modulation == 'turbo':
        tune_turbo(session, port, freq, sr, fec)
    elif modulation == 'dvbs2':
        tune_dvbs2(session, port, freq, sr, fec)
    else:
        raise ('invalid modulation type')

    return

def select_service(session, sid):
    vars = netsnmp.VarList(
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.4.1.0', sid, 'INTEGER')
            )

    print 'Configure program service id...'
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    return

def select_channel(session, vct, vcn):
    vars = netsnmp.VarList(
            netsnmp.Varbind('iso', '3.6.1.4.1.1166.1.621.4.1.0', sid, 'INTEGER')
            )

    print 'Configure virtual channel table/number...'
    for var in vars:
        print var.tag, var.iid, "=", var.val, '(',var.type,')'
    print session.set(vars)

    return

def show_status(session, self, refresh, csv):
    vars = netsnmp.VarList(
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.14.2.0'),     # Model

        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.9.1.1.0'),    # Unit Address
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.9.2.1.0'),    # Boot
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.9.2.2.0'),    # FPGA
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.9.2.3.0'),    # High
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.9.2.4.0'),    # Upgrade
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.9.3.5.0'),    # Uptime
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.9.3.6.0'),    # Build Date


        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.11.8.0'),     # Signal Quality
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.11.9.0'),     # Input Power
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.11.10.0'),    # SNR
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.11.11.0'),
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.11.12.0'),
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.11.13.0'),    # L-freq

        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.12.1.0'),     # LED
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.12.2.0'),     # LED
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.12.3.0'),     # LED
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.12.4.0'),     # LED
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.12.5.0'),     # LED

        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.11.2.0'),     # CA: 0: Encrypted, 1:?, 2: FP, 3: ZK
        netsnmp.Varbind('iso.3.6.1.4.1.1166.1.621.11.3.0'),     # CA: 0: Encrypted, 1:?, 2: FP, 3: ZK
        )

    results = session.get(vars)

    if csv == False:
        self.wfile.write("<html>")
        self.wfile.write("  <head>")
        self.wfile.write("  <title>DSR</title>")
        if refresh:
            self.wfile.write("  <meta http-equiv=\"refresh\" content=\"1\">")
        self.wfile.write("</head>")
        self.wfile.write("<body>")
        self.wfile.write("  <table>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Model:</td><td>%s</td>" % results[0] )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Unit Address:</td><td>%s</td>" % results[1] )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Firmware:</td><td>%s:%s:%s:%s</td>" % (results[2], results[3], results[4], results[5]) )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Uptime:</td><td>%s</td>" % results[6] )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Build date:</td><td>%s</td>" % results[7] )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td colspan='2'></td>")
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Signal Quality:</td><td>%s %%</td>" % results[8] )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Input Power:</td><td>%s db</td>" % results[9] )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>SNR:</td><td>%.1f dB</td>" % (float(results[10]) / 10) )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Frequency (L-band):</td><td>%.3f MHz</td>" % (float(results[13]) / 1000000) )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td colspan='2' />")
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Signal:</td><td>%s</td>" % results[14] )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Authorized:</td><td>%s : %s - %s</td>" % (results[15], results[19], results[20]) )
        self.wfile.write("    </tr>")
        self.wfile.write("    <tr>")
        self.wfile.write("      <td>Alarm:</td><td>%s</td>" % results[16] )
        self.wfile.write("    </tr>")
        self.wfile.write("  </table>")
        self.wfile.write("</body>")
        self.wfile.write("</html>")
    else:
        self.wfile.write("%s, %s, %s, %s, %s, %s, %s, %s" % 
                (float(results[13]) / 1000000), # L-band frequency
                results[8],                     # Signal Quality
                results[9],                     # Input Power
                (float(results[10]) / 10),      # SNR
                results[14],                    # Signal State
                results[15],                    # Authorized
                results[19]                     # Authorize State
                )

    return

class DSRHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            url = urlparse.urlparse(self.path)
            if url.path == "/favicon.ico":
                self.send_response(404)
                return

            # send code 200 response
            self.send_response(200)

            # send header first
            self.send_header('Content-type','text-html')
            self.end_headers()

            # split our path string
            pp = os.path.split(url.path)
            #print pp

            # parse our query string
            qs = urlparse.parse_qs(url.query)
            #print qs

            funct = pp[0] # first token is our function

            # Frontent identifier
            if len(pp) > 1 and len(pp[1]) > 0:
                instance = config[pp[1]]
            else:
                if 'fe' in qs:
                    fe = int(qs['fe'][0])
                else:
                    fe = 1
                if fe < 1 or fe > 65535:
                    raise ('invalid fe value')

                sections = config.sections()
                instance = config[sections[fe]]

            if funct == "/status":

                # create public snmp session for reading data
                session = netsnmp.Session( DestHost=instance.get('SnmpAddress'), Version=2, Community='public' )

                if 'refresh' in qs:
                    refresh = bool(qs['refresh'][0])
                else:
                    refresh = False

                if 'format' in qs:
                    format = qs['format'][0];
                    if format == 'csv':
                        csv = True
                    else:
                        csv = False
                else:
                    csv = False

                show_status(session, self, refresh, csv)

            elif funct == "/stream":

                # create private snmp session for writting data
                session = netsnmp.Session( DestHost=instance.get('SnmpAddress'), Version=2, Community='private' )

                # tune to mux
                tune(instance, session, qs)

                # give enough time to re-tune
                time.sleep(0.5)

                # sellect program or channel
                if 'sid' in qs:
                    sid = int(qs['sid'][0])
                    select_service(session, sid)
                elif 'vct' in qs and 'vcn' in qs:
                    vct = int(qs['vct'][0])
                    vcn = int(qs['vcn'][0])
                    select_channel(session, vct, vcn)

                # start streaming
                stream_url = instance.get('StreamUrl')
                print stream_url
                r = requests.get(stream_url, stream=True)
                for chunk in r.iter_content(chunk_size=512 * 1024):
                    if chunk: # filter out keep-alive new chunks
                        self.wfile.write(chunk)

            elif funct == "/tune":

                # create private snmp session for writting data
                session = netsnmp.Session( DestHost=instance.get('SnmpAddress'), Version=2, Community='private' )

                # tune to mux
                tune(instance, session, qs)

                # give enough time to re-tune
                time.sleep(0.5)

                # sellect program or channel
                if 'sid' in qs:
                    sid = int(qs['sid'][0])
                    select_service(session, sid)
                elif 'vct' in qs and 'vcn' in qs:
                    vct = int(qs['vct'][0])
                    vcn = int(qs['vcn'][0])
                    select_channel(session, vct, vcn)

                # crate public snmp session for reading
                session = netsnmp.Session( DestHost=instance.get('SnmpAddress'), Version=2, Community='public' )

                if 'format' in qs:
                    format = qs['format'][0];
                    if format == 'csv':
                        csv = True
                    else:
                        csv = False
                else:
                    csv = False

                show_status(session, self, False, csv)

            else:
                print "Unknown funct"

            return

        except IOError:
            self.send_error(404, 'file not found')

class MyServer(SocketServer.ThreadingMixIn,HTTPServer):
    pass

def run():
    print('reading config file...')
    config.read('dsrip.ini')

    print('http server is starting...')
    server_address = (
            config["server"].get("ListeningAddress", ''),
            config["server"].getint("ListeningPort", 80)
            )
    httpd = MyServer(server_address, DSRHTTPRequestHandler)
    print('http server is running...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
