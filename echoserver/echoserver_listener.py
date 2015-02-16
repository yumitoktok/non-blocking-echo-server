'''
Created on 15 Feb 2015

@author: guy
'''

from echoserver_connection import EchoServerConnection

import logging
logger = logging.getLogger(__name__)

import select

class EchoServerListener():
    
    def __init__(self, echoserver_socket):
        
        self._socket = echoserver_socket.getSocket()
        self._input  = [self._socket]       # Sockets from which we expect to read, initialised with open socket
        self._output = []                   # Sockets to which we expect to write
        self._err    = []                            
        self._connections = {}

    def addConnection(self, socket):
        server_connection = EchoServerConnection(socket)
        connection = server_connection.getConnection()
        self._input.append(connection)
        self._connections[connection]=server_connection
        return server_connection


    def listen(self):

        try:
            
            while self._input:

                logger.info("Waiting for socket event")
                read, write, exception = select.select(self._input, self._output, self._input)
                # No timeout - OK for the select to be blocking since this is the only loop
                # Check inputs for errors on each event loop
        
                # Inputs
                for s in read:
    
                    # Server socket ready to accept a connection
                    if s is self._socket:
                        server_connection = self.addConnection(s)
                        logger.info('New connection accepted from %s' % (server_connection.getClientAddress(),))

        
                    else: # Input from connection
                        server_connection = self._connections[s]
                        logger.info('New data from %s' % (server_connection.getClientAddress(),))
                        server_connection.recieve()
                        if server_connection.isOpen():
                            if server_connection.isPendingOutput() and s not in self._output:
                                logger.debug('Pending output to %s, adding to outputs' % (server_connection.getClientAddress(),))
                                self._output.append(server_connection.getConnection())
                        else: # No data, remove
                            logger.info('Empty data from %s, closing connection' % (server_connection.getClientAddress(),))
                            server_connection.close()
                            if s in self._output:  self._output.remove(s)
                            self._input.remove(s)
                            del self._connections[s]

                # Handle outputs
                for s in write:
                    server_connection = self._connections.get(s)
                    server_connection.send()
                    if s in self._output:  self._output.remove(s)
                
                
                # Handle "exceptional events"
                for s in exception:
                    
                    logger.exception("Exception from %s" % (s.getpeername(),))
                    server_connection = self._connections.get(s)
                    server_connection.close()
                    if s in self._output:  self._output.remove(s)
                    self._input.remove(s)
                    del self._connections[s]


        except KeyError as e:
            logger.exception("Server Connection not found: %s" %(e.message,))
            
    
        except Exception as e:
            logger.exception(e.message)
