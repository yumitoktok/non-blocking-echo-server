'''
Created on 15 Feb 2015

@author: guy
'''

import logging
logger = logging.getLogger(__name__)

from socket import error as socket_error

import Queue

class EchoServerConnection():
    
    def __init__(self, socket):
        self._connection, self._client_address = socket.accept()
        self._connection.setblocking(0)
        self._output_queue = Queue.Queue()
        self._wait_queue   = Queue.Queue()
        
    def getConnection(self):
        return self._connection
    
    def getClientAddress(self):
        return self._client_address
    
    def recieve(self):
        try:
            data = self._connection.recv(1024) # Only receive 1024 bytes per line. Sensible to limit to help mitigate DenialOfService
            if data:
                
                # TODO: Check data is meaningful & secure
                logger.info("Received %s from %s" % (data, self._connection.getpeername()))
                           
                nl = data.rfind("\n")
                if nl > 0:
                    self.buildOutputQueue(data[:nl])
                    if nl >= len(data):
                        self._wait_queue.put(data[nl:])
                        
                else:
                    logger.debug("No carriage return, storing")
                    self._wait_queue.put(data)
                    
            else:
                logger.info("No data recieved from %s, closing connection" % (self._connection.getpeername(),))
                self.close()
                
        except socket_error as serr:
            raise EchoServerConnectionDisconnectException(self._connection, "%s" % (serr.errno,))
  
    
    def flush(self):
        # Check chunks
        try:
            while True:
                self._connection.send(self._output_queue.get_nowait())
        except Queue.Empty:
            pass
        except socket_error as serr:
            raise EchoServerConnectionDisconnectException(self, "%s" % (serr.errno,))

                
                
    
    def buildOutputQueue(self,last):
        try:    
            while True:
                self._output_queue.put(self._wait_queue.get_nowait())
        except Queue.Empty:
            self._output_queue.put(last)
         
           
    def close(self):
        if (self._connection):
            self._connection.close()
            self._connection = None
            
    def isOpen(self):
        return bool(self._connection)
    
    def isPendingOutput(self):
        return not self._output_queue.empty() 
        
    def isWaitingOutput(self):
        return not self._wait_queue.empty()     
    
    
     
class EchoServerConnectionDisconnectException(Exception):
    
    def __init__(self, c, message):
        self.echoserver_connection = c
        self.message = message
    
       
    