#!/usr/bin/env python
import argparse
import sys
import random
import socket
from time import gmtime, strftime
from urlparse import urlparse, parse_qs

# for POST request handling
from StringIO import StringIO
import cgi

# file selection and Jinja templates
import jinja2
import os

## for the wsgi app
import app

## other apps
import quixote
from quixote.demo.altdemo import create_publisher #login demo
import imageapp
from wsgiref.validate import validator

# global variables for command line app argument input
_app_init_complete = False
IMAGE_APP = 'image'
MY_APP = 'myapp'
QUIXOTE_ALTDEMO_APP = 'altdemo'

VALID_APPS = [QUIXOTE_ALTDEMO_APP, MY_APP, IMAGE_APP]

# parse command line arguments
parser = argparse.ArgumentParser(description="Process app name and port args")
parser.add_argument('-A', nargs='?', metavar='application', default = MY_APP, \
                    help='Choose an application to run on the server.')
parser.add_argument('-p', metavar='port', nargs='?', default=random.randint(8000, 9999), \
                    type=int, help='Choose a port to on which to run host the server')
args = parser.parse_args()

def init_app(current_app):
    global _app_init_complete

    if(current_app == MY_APP):
        return app.make_app()
    elif (current_app == QUIXOTE_ALTDEMO_APP):
        if not _app_init_complete:
            p = create_publisher()
            _app_init_complete = True
        return quixote.get_wsgi_app()
    elif (current_app == IMAGE_APP):
        if not _app_init_complete:
            imageapp.setup()
            p = imageapp.create_publisher()
            _app_init_complete = True
        return quixote.get_wsgi_app()

def main(socket_module = socket):
    s = socket_module.socket()         # Create a socket object
    host = socket.getfqdn() # Get local machine name

    # Use command line arguments
    port = args.p
    current_app = args.A

    if current_app not in VALID_APPS:
        print "%s is not a valid application." % current_app
        exit()

    s.bind((host, port))        # Bind to the port

    print 'Starting server on', host, port
    print 'The Web server URL for this would be http://%s:%d/' % (host, port)

    s.listen(5)                 # Now wait for client connection.

    print 'Entering infinite loop; hit CTRL-C to exit'

    while True:
        # Initialize environ dict
        environ = get_environ(port)
        # Establish connection with client.    
        c, (client_host, client_port) = s.accept()
        print 'Got connection from', client_host, client_port
        handle_connection(c, environ, current_app)

# parses incoming request data and serves appropriate page data
def handle_connection(conn, environ, current_app):
    # Borrowed some WSGI compatibility code from github user 'maxwellgbrown'
    # Start reading in data from the connection
    read = conn.recv(1)
    while read[-4:] != '\r\n\r\n':
        read += conn.recv(1)

    request, data = read.split('\r\n',1)

    headers = {}
    for line in data.split('\r\n')[:-2]:
        k, v = line.split(': ',1)
        headers[k.lower()] = v

    parsed_url = urlparse(request.split(' ', )[1])
    
    environ['PATH_INFO'] = parsed_url[2]
    environ['QUERY_STRING'] = parsed_url[4]
    environ['SCRIPT_NAME'] = ''
    if 'cookie' in headers:
        environ['HTTP_COOKIE'] = headers['cookie']

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
    application = init_app(current_app)
    
    response_html = application(environ, start_response)
    for html in response_html:
        conn.send(html)
    
    # close the connection
    conn.close()

# Generates environ dict for use in this class and testing
def get_environ(port = 9999):
    environ = {}

    environ['SERVER_NAME'] = socket.getfqdn()
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
