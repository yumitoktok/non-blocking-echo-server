import socket
import sys
from random import choice
from string import ascii_lowercase

"""
TEST
One huge string
"""

MESSAGE_LENGTH = 1000000
MESSAGE_SRC = list(ascii_lowercase)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address


sockets = [
           socket.socket(socket.AF_INET, socket.SOCK_STREAM),
           socket.socket(socket.AF_INET, socket.SOCK_STREAM)
           ]



messages = [
            ''.join(choice(MESSAGE_SRC) for _ in xrange(MESSAGE_LENGTH)),
            ''.join(choice(MESSAGE_SRC) for _ in xrange(MESSAGE_LENGTH))
            ]


for i in range(len(sockets)):
    s = sockets[i]
    m = messages[i]
    s.connect(server_address)
    print "SENDING LARGE MESSAGE\n\n%s" % (m, )
    s.sendall(m)  
    s.send("\n")

while True:
    if (len(sockets)==0): break
    for i in range(len(sockets)):
        s = sockets[i]
        print "RECEIVING RESPONSE FROM %s:\n\n" % (i+1,)
        data = s.recv(1024)
        if data: print data
        else: 
            del sockets[i]
        