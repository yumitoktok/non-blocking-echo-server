Write an "asynchronous" non-blocking tcp echo server in python (2 or 3)
-------------------------------------------------------------------------

Implement a python process that listens on a server socket for incoming TCP connections.

It should echo all lines of data back to the socket. ie: if the
connected client sends the string of bytes 'hello\n' then the server
should send 'hello\n' back to the client over the same socket.
The server should only echo the response on receipt of a line break
'\n' not before. It will only echo full lines. The client may send any
number of lines before disconnecting.

The server should handle multiple concurrent connections without using
threads/processes or any other networking library including python's
asyncio; it should only use socket and select.
If one connection is idle then the server must be able to serve the
other connections whilst it is waiting for a response.

This is intended to be a long-running server so pay attention to the
entire lifecycle of the incoming connections.

Consider that a whole line may not be able to be sent to the client all at once.
Be careful not to block when accepting new connections.

The server only need perform as described above; no need to engineer
for a more generalised solution, a solution specialised to only the
points above is fine.