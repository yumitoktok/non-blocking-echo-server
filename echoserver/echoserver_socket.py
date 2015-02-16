'''
Created on 15 Feb 2015

@author: guy
'''

import socket
import logging

logger = logging.getLogger(__name__)

class EchoServerSocket():
    
    def __init__(self, port, host):
        self._HOST     = host
        self._PORT     = port
        self._IP       = socket.AF_INET     # IPv4
        self._PROTOCOL = socket.SOCK_STREAM # TCP 
        self._BACKLOG  = 5                  # Maximum number of queued connections (assumed)
        self._socket   = None
        
    
    def open(self):
        try:
            logger.info("Binding socket to %s:%s" % (self._HOST, self._PORT))
            s = socket.socket(self._IP, self._PROTOCOL)
            s.setblocking(False)
            s.bind((self._HOST, self._PORT))
            s.listen(self._BACKLOG)
            self._socket = s
            
        except socket.error as e: 
            s.close()
            raise EchoServerSocketException("Could not open EchoServerSocket on %s:%s / %s" % (self._HOST, self._PORT, e.message) )

    def isOpen(self):
        logger.info("Checking socket open: %s" % (bool(self._socket),))
        return bool(self._socket)

    def close(self):
        logger.info("Closing socket...")
        if self._socket: 
            logger.info("Socket open, closing.")
            self._socket.close()
            self.socket = None
        

    def getSocket(self):
        if (self.isOpen()):
            return self._socket
        else:
            raise EchoServerSocketException("EchoServerSocket not opened")

    

class EchoServerSocketException(Exception):
    pass
    