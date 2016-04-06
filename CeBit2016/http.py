#!/usr/bin/python2
# -*- coding: UTF-8 -*-
#
# see main.py for copyright, contacts and version information
#

# Python 2:
import BaseHTTPServer
# Python 3:
# import http.server
import SocketServer
import socket

# taken from http://www.python-forum.de/viewtopic.php?t=2647
class ThreadingServer( SocketServer.ThreadingTCPServer ):
    '''
    Verbesserung des Standard Servers:
     - Ermöglicht das Abarbeiten mehrere Anfragen parallel (z.B. Download mehrere Dateien gleichzeitig)
     - Ermöglicht das Einschränken des IP-Bereiches aus denen der Server Anfragen behandelt
    '''
    allow_reuse_address = 1    # Seems to make sense in testing environment

    def __init__(self, server_address, request_handler, AllowIPs):
        SocketServer.ThreadingTCPServer.__init__(self, server_address, request_handler)
        self.AllowIPs = [mask.split('.') for mask in AllowIPs]

    def server_bind(self):
        # Override server_bind to store the server name. (Parallele Anfragen)
        SocketServer.ThreadingTCPServer.server_bind(self)
        host, port = self.socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

    def verify_request(self, dummy, client_address):
        # Checkt ob die IP-Adresse der Anfrage in 'AllowIPs' vorhanden ist

        def check_ip(mask):
            for mask_part, ip_part in zip(mask, ip):
                if mask_part != ip_part and mask_part != '*':
                    return False
            return True

        ip = client_address[0].split('.')

        for mask in self.AllowIPs:
            if check_ip(mask):
                return True

        print("IP [%s] not allowed!" % client_address)

        # Beugt DOS Attacken vor, indem die Rückmeldung verzögert und
        # somit CPU-Zeit freigegeben wird.
        time.sleep(1)

        return False


