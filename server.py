#!/usr/bin/env python
import random
import socket
import time
import urlparse

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

# serves index page data
def index(conn, request):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') # Separate headers from body
    conn.send('<a href="/content">CONTENT</a><br>')
    conn.send('<a href="/file">FILE</a><br>')
    conn.send('<a href="/image">IMAGE</a><br>')
    conn.send('<a href="/form">FORM</a><br>')
    conn.close()

# serves basic form page
def serve_form(conn, request):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') # Separate headers from body
    # conn.send("<form action='/submit' method='GET'>")
    # conn.send("First Name: <input type='text' name='firstname'><br>")
    # conn.send("Last Name: <input type='text' name='lastname'><br>")
    # conn.send("<input type='submit' value='Submit'>")
    # conn.send("</form><br>")
    conn.send("<form action='/submit' method='POST'>")
    conn.send("First Name: <input type='text' name='firstname'><br>")
    conn.send("Last Name: <input type='text' name='lastname'><br>")
    conn.send("<input type='submit' value='Submit'>")
    conn.send("</form>")
    conn.close()

# parses post submission from basic form
def handle_post_submit(conn, request):
    body = request.split("\r\n\r\n")
    parsed_query = urlparse.parse_qs(body[1])
    first_name = parsed_query['firstname'][0] # get firstname field from url as string
    last_name = parsed_query['lastname'][0] # get lastname field from url as string
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') # Separate headers from body
    conn.send('<h1>Hello Mr. %s %s.</h1>'%(first_name, last_name))
    conn.close()

# parses get submission from basic form
def handle_get_submit(conn, request):
    params = request.split(' ')
    parsed_url = urlparse.urlparse(params[1])
    parsed_query = urlparse.parse_qs(parsed_url.query)
    first_name = parsed_query['firstname'][0] # get firstname field from url as string
    last_name = parsed_query['lastname'][0] # get lastname field from url as string
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') # Separate headers from body
    conn.send('<h1>Hello Mr. %s %s.</h1>'%(first_name, last_name))
    conn.close()

def handle_basic_post(conn, request):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') # Separate headers from body
    conn.send('<h1>Hello, world.</h1>')
    conn.close()

# serves 'content' page
def serve_content(conn, request):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') # Separate headers from body
    conn.send('<h1>Hello, world.</h1>This is zhopping\'s Web server.')
    conn.close()

# serves "image" page
def serve_image(conn, request):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') # Separate headers from body
    conn.send('<h1>Image Example</h1><br>')
    conn.send('<img border="0" src="http://static3.wikia.nocookie.net/__cb20130826211346/creepypasta/images/0/01/DOGE.png" alt="DOGE">')
    conn.close()

# serves "file" page
def serve_file(conn, request):
    conn.send('HTTP/1.0 200 OK\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') # Separate headers from body
    conn.send('<h1>File</h1><br>')
    conn.close()

def send_404_error(conn, request):
    conn.send('HTTP/1.0 404 Not Found\r\n')
    conn.send('Content-type: text/html\r\n')
    conn.send('\r\n') #separate headers from body
    conn.send('<h1>Error 404 Page Not Found</h1>')
    conn.close()

# parses incoming request data and serves appropriate page data
def handle_connection(conn):
    request = conn.recv(1000)
    params = request.split(' ')
    if request.startswith('GET'):
        parsed_url = urlparse.urlparse(params[1])
        path = parsed_url.path
        if path == '/':
            index(conn, request)
        elif path == '/form':
            serve_form(conn, request)
        elif path.startswith('/submit'):
            handle_get_submit(conn, request)
        elif path == '/content':
            serve_content(conn, request)
        elif path == '/file':
            serve_file(conn, request)
        elif path == '/image':
            serve_image(conn, request)
        else:
            send_404_error(conn, request)
    elif params[0] == 'POST':
        parsed_url = urlparse.urlparse(params[1])
        path = parsed_url.path
        if path.startswith('/submit'):
            handle_post_submit(conn, request)
        else:
            handle_basic_post(conn, request)

if __name__ == '__main__':
    main()
