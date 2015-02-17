# -*- coding: utf-8 -*-

import socket
import sys

"""
TEST
Binary data
"""

message = "\x01sagr\x00\x00\x00\x00\x00\x00\x00\x00zvashj4$\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00grwqwrg\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server_address)
s.settimeout(2)
  
print "SENDING BINARY DATA"
s.send(message)  
s.send("\n")
print "RECEIVING RESPONSE:\n\n"
data = s.recv(1024)
print data