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

# parses incoming request data and serves appropriate page data
def handle_connection(conn):
    request = ""
    bytes_read = 0
    
    while("\r\n\r\n" not in request):
        request += conn.recv(1)
        bytes_read += 1

    print "BYTES READ: " + str(bytes_read)

    if not request:
        conn.close()
        return

    request_components = request.split(' ')
    request_type = 'text/html' # default request type
    path = '/' # default request path

    if len(request_components) > 0:
        request_type = request.split(' ')[0]
    if len(request_components) > 1:
        path = request.split(' ')[1]

    parsed_url = urlparse.urlparse(path)
    # print "Request Information ----------"
    # print "Path: " + path
    # print "Type: " + request_type
    # print "Params: " + parsed_url.params
    # print "Query: " + parsed_url.query

    #raw_request, raw_headers= request.split('\r\n',1)    # split request line and headers
    #headers = Message(StringIO(raw_headers))   # headers can be thought as a dictionary

    


    if request_type == "POST":
        headers = {}
        raw_headers = request.splitlines()[1:] # Gets header lines.
        for header in raw_headers:
            try:
                k, v = header.split(': ', 1)
            except:
                continue
            headers[k.lower()] = v

        # Extracts message from request.
        payload = ''
        while len(payload) < int(headers['content-length']):
            payload += conn.recv(1)

        if("content-type" in headers.keys()):
            if("application/x-www-form-urlencoded" in headers["content-type"]):
                handle_post_request(conn, path, payload)
            elif("multipart/form-data" in headers["content-type"]):
                environ = {}
                environ['REQUEST_METHOD'] = 'POST'

                form = cgi.FieldStorage(headers=headers, fp=StringIO(payload), environ=environ)
                print form.keys()
                handle_multipart_post_request(conn, path, form) 
        else:
            handle_post_request(conn, path, payload)

    elif request_type == "GET":
        handle_get_request(path, parsed_url, conn)

    else:
        send_404_error(conn)
        # Should serve 'bad request' page?

    conn.close()



# parses post submission from basic form
def handle_post_request(conn, path, payload):
    if path.startswith('/submit'):
        parsed_query = parse_qs(payload)
        handle_form_submit(parsed_query['firstname'][0], parsed_query['lastname'][0], conn)
    else:
        send_404_error(conn)

def handle_multipart_post_request(conn, path, form):
    if(path == '/submit'):
        handle_form_submit(form.getvalue("'firstname'"),form.getvalue("'lastname'"),conn)
    else:
        send_404_error(conn)

# parse and correctly serve all get requests
def handle_get_request(path, parsed_url, conn):
    parsed_path = parsed_url.path

    if(path.split('?')[0] == "/submit"):
        form_data = parse_qs(parsed_path.query)
        handle_form_submit(form_data["firstname"][0],form_data["lastname"][0],conn)
        return

    if path[len(path) - 1] == '/':
        path = path + "index.html"
    if path[0] == '/':
        path = path[1:]

    dirname, filename = os.path.split(os.path.abspath(__file__))
    dirname = dirname + "/"

    print "DIRNAME: " + dirname

    loader = jinja2.FileSystemLoader(dirname + "templates")
    env = jinja2.Environment(loader=loader,autoescape=True)

    print "Path:",path

    try:
        template = env.get_template(path)
        html = template.render()
        conn.send(http_header())
        conn.send(html)
    except:
        template = env.get_template("404.html")
        conn.send(http_404_header()) # Could not find file to serve
        conn.send(template.render())

    print 'request handled'

def handle_form_submit(first_name, last_name, conn):
    conn.send(http_header())
    conn.send('<h1>Hello Mr. %s %s.</h1>'%(first_name, last_name))
    conn.close()


def send_404_error(conn):
    conn.send(http_404_header())
    conn.send('<h1>Error 404 Page Not Found</h1>')
    conn.close()

def http_header():
    return 'HTTP/1.0 200 OK\r\n' + \
            'Content-type: text/html\r\n' + \
            '\r\n'

def http_404_header():
    return 'HTTP/1.0 404 Not found\r\n' + \
                    'Content-type: text/html\r\n' + \
                    'Connection: close\r\n' + \
                    '\r\n'


if __name__ == '__main__':
    main()
