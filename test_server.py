import server

class FakeConnection(object):
    """
    A fake connection class that mimics a real TCP socket for the purpose
    of testing socket I/O.
    """
    def __init__(self, to_recv):
        self.to_recv = to_recv
        self.sent = ""
        self.is_closed = False

    def recv(self, n):
        if n > len(self.to_recv):
            r = self.to_recv
            self.to_recv = ""
            return r
            
        r, self.to_recv = self.to_recv[:n], self.to_recv[n:]
        return r

    def send(self, s):
        self.sent += s

    def close(self):
        self.is_closed = True

def test_handle_connection_bad_request_type():

  payload = "BADREQUEST\r\n"

  conn = FakeConnection(
    "POST /doge HTTP/1.0\r\n" + \
    "Content-Type: application/x-www-form-urlencoded\r\n" + \
    "Content-Length: " + str(len(payload)) + "\r\n\r\n" + \
    payload)
  expected_return = 'HTTP/1.0 404 Not Found\r\nContent-type: text/html\r\n\r\n' + \
  '<!DOCTYPE html>\n<html>\n\n<head>\n\n  <title>  Web Server - Error Page  </title>\n\n</head>\n\n' + \
  '<body>\n\n\n<h1>Error Page</h1>\nThis page does not exist\n\n\n</body>\n </html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_form_get():
  conn = FakeConnection("GET /submit?firstname=Beautiful&lastname=Shibe HTTP/1.0\r\n\r\n")
  expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + \
                    '<!DOCTYPE html>\n<html>\n\n<head>\n\n  ' + \
                    '<title>  Web Server - Submit Page  </title>\n\n</head>\n\n' + \
                    '<body>\n\n\n<h1>Submit Page</h1>\nHello Beautiful Shibe\n\n\n</body>\n </html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_form_explicit_post():
  payload = "firstname=Beautiful&lastname=Shibe"

  conn = FakeConnection(
    "POST /submit HTTP/1.0\r\n" + \
    "Content-Type: application/x-www-form-urlencoded\r\n" + \
    "Content-Length: " + str(len(payload)) + "\r\n\r\n" + \
    payload)
  expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + \
                    '<!DOCTYPE html>\n<html>\n\n<head>\n\n  ' + \
                    '<title>  Web Server - Submit Page  </title>\n\n</head>\n\n' + \
                    '<body>\n\n\n<h1>Submit Page</h1>\nHello Beautiful Shibe\n\n\n</body>\n </html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_multipart_form_post():
  payload = "--AaB03x\r\n" + \
        "Content-Disposition: form-data; name=firstname;\r\n\r\n" + \
        "Beautiful\r\n" + \
        "--AaB03x\r\n" + \
        "Content-Disposition: form-data; name=lastname;\r\n\r\n" + \
        "Shibe\r\n" + \
        "--AaB03x--\r\n"

  conn = FakeConnection("POST /submit HTTP/1.0\r\n" + \
              "Content-Length: " + (str(len(payload))) + "\r\n"  + \
              "Content-Type: multipart/form-data; boundary=AaB03x\r\n\r\n" + payload)
  expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + \
                    '<!DOCTYPE html>\n<html>\n\n<head>\n\n  ' + \
                    '<title>  Web Server - Submit Page  </title>\n\n</head>\n\n' + \
                    '<body>\n\n\n<h1>Submit Page</h1>\nHello Beautiful Shibe\n\n\n</body>\n </html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)


def test_handle_connection_bad_form_post():
  payload = "firstname=Beautiful&lastname=Shibe\r\n"

  conn = FakeConnection(
    "POST /doge HTTP/1.0\r\n" + \
    "Content-Type: application/x-www-form-urlencoded\r\n" + \
    "Content-Length: " + str(len(payload)) + "\r\n\r\n" + \
    payload)
  expected_return = 'HTTP/1.0 404 Not Found\r\nContent-type: text/html\r\n\r\n' + \
  '<!DOCTYPE html>\n<html>\n\n<head>\n\n  <title>  Web Server - Error Page  </title>\n\n</head>\n\n' + \
  '<body>\n\n\n<h1>Error Page</h1>\nThis page does not exist\n\n\n</body>\n </html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_bad_multipart_form_post():
  payload = "--AaB03x\r\n" +\
    "Content-Disposition: form-data; name='firstname'\r\n" +\
    "\r\n" +\
    "Beautiful\r\n" +\
    "--AaB03x\r\n" +\
    "Content-Disposition: form-data; name='lastname'\r\n" +\
    "\r\n" +\
    "Shibe\r\n" +\
    "--AaB03x\r\n"

  conn = FakeConnection("POST /dingus HTTP/1.0\r\n" + \
                        "Content-Length: " + (str(len(payload))) + "\r\n"  + \
                        "Content-Type: multipart/form-data; boundary=AaB03x\r\n\r\n" + \
                        payload)
  expected_return = 'HTTP/1.0 404 Not Found\r\nContent-type: text/html\r\n\r\n' + \
  '<!DOCTYPE html>\n<html>\n\n<head>\n\n  <title>  Web Server - Error Page  </title>\n\n</head>\n\n' + \
  '<body>\n\n\n<h1>Error Page</h1>\nThis page does not exist\n\n\n</body>\n </html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_bad_page():

  conn = FakeConnection("GET /doge.html HTTP/1.0\r\n\r\n")
  expected_return = 'HTTP/1.0 404 Not Found\r\nContent-type: text/html\r\n\r\n' + \
  '<!DOCTYPE html>\n<html>\n\n<head>\n\n  <title>  Web Server - Error Page  </title>\n\n</head>\n\n' + \
  '<body>\n\n\n<h1>Error Page</h1>\nThis page does not exist\n\n\n</body>\n </html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

# Test a basic GET call.
def test_handle_connection_root():
  conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
  expected_return = "HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n" + \
                    "<!DOCTYPE html>\n<html>\n\n<head>\n\n" + \
                    "  <title>  Web Server - Index Page  </title>\n\n</head>\n\n<body>\n\n\n" + \
                    "<h1>Hello World!</h1>\nThis is zhopping's Web Server.\n<p>\n" + \
                    "<a href='/content'>Content</a><br>\n<a href='/files'>Files</a><br>\n" + \
                    "<a href='/images'>Images</a><br>\n<a href='/form'>Form</a>\n\n\n</body>\n </html>"

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_content():
  conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
  expected_return = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n' + \
                    '<!DOCTYPE html>\n<html>\n\n<head>\n\n  ' + \
                    '<title>  Web Server - Content Page  </title>\n\n' + \
                    '</head>\n\n<body>\n\n\n<h1>Content Page</h1>\nThis is the content page\n\n\n</body>\n </html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_file():
  conn = FakeConnection("GET /files HTTP/1.0\r\n\r\n")
  expected_return = 'HTTP/1.0 200 OK\r\n' + \
          'Content-type: text/plain\r\n' + \
          '\r\n' + \
          'I like watermelon.\n' + \
          'I like strawberries.\n' + \
          'I like blueberries.\n' + \
          'I like lemons.\n' + \
          'I like raspberries.\n' + \
          'I don\'t care much for honeydew.'

  server.handle_connection(conn, server.get_environ(), 'myapp')

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_image():
  conn = FakeConnection("GET /images HTTP/1.0\r\n\r\n")
  expected_return = u'HTTP/1.0 200 OK\r\n' + \
          u'Content-type: text/html\r\n' + \
          u'\r\n' + \
          u'<html><body><h1>Image</h1><br>\n' + \
          '<img border="0" src="http://static3.wikia.nocookie.net/__cb20130826211346/creepypasta/images/0/01/DOGE.png" alt="DOGE">\n' + \
          '</body></html>'

  server.handle_connection(conn, server.get_environ(), 'myapp')
   # Ensure that a jpg file is received
  if ('HTTP/1.0 200 OK' and 'Content-type: image/jpeg') not in conn.sent:
    assert False
  else:
    pass

  #assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)
