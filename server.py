# TODO: external logging config


import logging
logging.basicConfig(level=logging.INFO) # Put logging config in before importing other modules

import argparse
import sys

from echoserver.echoserver_socket import EchoServerSocket, EchoServerSocketException
from echoserver.echoserver_listener import EchoServerListener

logger = logging.getLogger(__name__)

try:
    parser = argparse.ArgumentParser(description='Create non-blocking tcp echo server ')
    parser.add_argument('--port', default=10000, type=int, help="Port to listen on", dest="port", action="store")
    parser.add_argument('--host', default="localhost", type=str, help="Host name to listen as", dest="host", action="store")
    args = parser.parse_args()
    
    socket = EchoServerSocket(args.port, args.host)
    socket.open()

    listener = EchoServerListener(socket)
    listener.listen()
    
except EchoServerSocketException as e:
    logging.exception(e.message)
    sys.exit()

except Exception as e:
    logging.exception(" Unknown Error: %s" % (e.message,))
    sys.exit()

