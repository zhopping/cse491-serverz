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
	request_type = request.split(' ')[0]
	path = request.split(' ')[1]


	response_body_raw_root = 'HTTP/1.0 200 OK\r\n' + \
					'Content-type: text/html\r\n' + \
					'\r\n' + \
					'<html><body>' + \
					'<h1>Hello world!</h1>This is xavierdhjr\'s Web server.' + \
					'<br/><a href="/content">Content</a>' + \
					'<br/><a href="/file">File</a>' + \
					'<br/><a href="/image">Image</a>' + \
					'</body></html>'
	response_body_raw_content = 'HTTP/1.0 200 OK\r\n' + \
					'Content-type: text/html\r\n' + \
					'\r\n' + \
					'<html><body><h1>Content</h1>This is xavierdhjr\'s Web server.</body></html>'
	response_body_raw_file = 'HTTP/1.0 200 OK\r\n' + \
					'Content-type: text/html\r\n' + \
					'\r\n' + \
					'<html><body><h1>File</h1>This is xavierdhjr\'s Web server.</body></html>'
	response_body_raw_image = 'HTTP/1.0 200 OK\r\n' + \
					'Content-type: text/html\r\n' + \
					'\r\n' + \
					'<html><body><h1>Image</h1>This is xavierdhjr\'s Web server.</body></html>'
	
	if request_type == "POST":
		conn.send("hello world")
		conn.close()
		return
		
	if path == '/':
		conn.send(response_body_raw_root)
	if path == '/content':
		conn.send(response_body_raw_content)
	if path == '/file':
		conn.send(response_body_raw_file)
	if path == '/image':
		conn.send(response_body_raw_image)
		
	conn.close()
	
if __name__ == '__main__':
   main()
