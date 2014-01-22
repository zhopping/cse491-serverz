#!/usr/bin/env python
import random
import socket
import time

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c)

def handle_connection(conn):
    request = conn.recv(1000)
    params = request.split(' ')
    if params[0] == 'GET':
        path = request.split(' ')[1]
        if path == '/':
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-type: text/html\r\n')
            conn.send('\r\n') # Separate headers from body
            conn.send('<a href="/content">CONTENT</a><br>')
            conn.send('<a href="/file">FILE</a><br>')
            conn.send('<a href="/image">IMAGE</a><br>')
            conn.close()
        elif path == '/content':
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-type: text/html\r\n')
            conn.send('\r\n') # Separate headers from body
            conn.send('<h1>Hello, world.</h1>This is zhopping\'s Web server.')
            conn.close()
        elif path == '/file':
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-type: text/html\r\n')
            conn.send('\r\n') # Separate headers from body
            conn.send('<h1>File</h1><br>')
            conn.close()
        elif path == '/image':
            conn.send('HTTP/1.0 200 OK\r\n')
            conn.send('Content-type: text/html\r\n')
            conn.send('\r\n') # Separate headers from body
            conn.send('<h1>Image Example</h1><br>')
            conn.send('<img border="0" src="http://static3.wikia.nocookie.net/__cb20130826211346/creepypasta/images/0/01/DOGE.png" alt="DOGE">')
            conn.close()
        else:
            pass # should send 404 error
    elif params[0] == 'POST':
        conn.send('HTTP/1.0 200 OK\r\n')
        conn.send('Content-type: text/html\r\n')
        conn.send('\r\n') # Separate headers from body
        conn.send('<h1>Hello, world.</h1>')
        conn.close()

if __name__ == '__main__':
    main()
