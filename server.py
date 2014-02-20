#!/usr/bin/env python
import random
import socket
import time
import urlparse
import cgi
import os
import jinja2
from mimetools import Message
from StringIO import StringIO
import app

import quixote
from quixote.demo import create_publisher
#from quixote.demo.mini_demo import create_publisher
#from quixote.demo.altdemo import create_publisher

_the_app = None
def make_app():
    global _the_app

    if _the_app is None:
        p = create_publisher()
        _the_app = quixote.get_wsgi_app()

    return _the_app

def main():
    s = socket.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name
    port = random.randint(8000, 9999)
    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'

    environ = get_environ(port)
    while True:
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, environ)

# parses incoming request data and serves appropriate page data
def handle_connection(conn, environ):
    # Borrowed WSGI compatibility code from github user 'maxwellgbrown'
    # Start reading in data from the connection
    read = conn.recv(1)
    while read[-4:] != '\r\n\r\n':
        read += conn.recv(1)

    request, data = read.split('\r\n',1)

    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ',1)
        headers[k.lower()] = v

    parsed_url = urlparse.urlparse(request.split(' ', )[1])
    
    environ['PATH_INFO'] = parsed_url[2]
    environ['QUERY_STRING'] = parsed_url[4]
    environ['SCRIPT_NAME'] = ''
    content = ''
    if request.startswith('POST '):
        environ['REQUEST_METHOD'] = 'POST'
        environ['CONTENT_LENGTH'] = headers['content-length']
        environ['CONTENT_TYPE'] = headers['content-type']
        # read the remaining data from http request to construct wsgi.input
        while len(content) < int(headers['content-length']):
            content += conn.recv(1)
    
    else:
        environ['REQUEST_METHOD'] = 'GET'
        environ['CONTENT_LENGTH'] = 0
    
    environ['wsgi.input'] = StringIO(content)
    
    
    def start_response(status, response_headers):
        conn.send('HTTP/1.0 %s\r\n' % status)
        for header in response_headers:
            conn.send('%s: %s\r\n' % header)
        conn.send('\r\n')

    # make the app  
    application = app.make_app()
    
    response_html = application(environ, start_response)
    conn.send(response_html)
    
    # close the connection
    conn.close()

# Generates environ dict for use in this class and testing
def get_environ(port = 9999):
    environ = {}

    environ['SERVER_NAME'] = "beans"
    environ['SERVER_PORT'] = str(port)
    environ['wsgi.version'] = (1,0)
    environ['wsgi.errors'] = StringIO()
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = False
    environ['wsgi.run_once'] = False
    environ['wsgi.url_scheme'] = 'http'
    environ['SCRIPT_NAME'] = ""

    return environ

if __name__ == '__main__':
    main()
