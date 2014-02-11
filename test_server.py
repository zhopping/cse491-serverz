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

  conn = FakeConnection(
    "DOGE /doge HTTP/1.0\r\n" + \
    "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
    "LOLTHISREQUESTISBAD")
  expected_return = u'HTTP/1.0 404 Not found\r\n' + \
          'Content-type: text/html\r\n' + \
          'Connection: close\r\n' + \
          '\r\n' + \
          'Invalid request syntax'

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_form_get():
  conn = FakeConnection("GET /submit?firstname=Beautiful&lastname=Shibe HTTP/1.0\r\n\r\n")
  expected_return = 'HTTP/1.0 200 OK\r\n' + \
      'Content-type: text/html\r\n' + \
      '\r\n' +\
      "<html><body>" + \
      "<h1>Hello Mr. Beautiful Shibe.</h1>" + \
      "</body></html>"

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_form_post():
  conn = FakeConnection(
    "POST /submit HTTP/1.0\r\n\r\n" + \
    "firstname=Beautiful&lastname=Shibe")
  expected_return = 'HTTP/1.0 200 OK\r\n' + \
      'Content-type: text/html\r\n' + \
      '\r\n' +\
      "<html><body>" + \
      "<h1>Hello Mr. Beautiful Shibe.</h1>" + \
      "</body></html>"

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_form_explicit_post():
  conn = FakeConnection(
    "POST /submit HTTP/1.0\r\n" + \
    "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
    "firstname=Beautiful&lastname=Shibe")
  expected_return = 'HTTP/1.0 200 OK\r\n' + \
      'Content-type: text/html\r\n' + \
      '\r\n' +\
      "<html><body>" + \
      "<h1>Hello Mr. Beautiful Shibe.</h1>" + \
      "</body></html>"

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_multipart_form_post():
  conn = FakeConnection(
    "POST /submit HTTP/1.0\r\n" + \
    "Content-Type: multipart/form-data; boundary=AaB03x\r\n\r\n" +\
    "--AaB03x\r\n" +\
    "Content-Disposition: form-data; name='firstname'\r\n" +\
    "\r\n" +\
    "Beautiful\r\n" +\
    "--AaB03x\r\n" +\
    "Content-Disposition: form-data; name='lastname'\r\n" +\
    "\r\n" +\
    "Shibe\r\n" +\
    "--AaB03x\r\n" +\
    "Content-Disposition: form-data; name='files'; filename='file1.txt'\r\n" +\
    "Content-Type: text/plain\r\n" +\
    "\r\n" +\
    "... contents of file1.txt ...\r\n" +\
    "--AaB03x--\r\n"
    )
  expected_return = 'HTTP/1.0 200 OK\r\n' + \
        'Content-type: text/html\r\n' + \
        '\r\n' +\
        "<html><body>" + \
        "<h1>Hello Mr. Beautiful Shibe.</h1>" + \
        "</body></html>"

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)


def test_handle_connection_bad_form_post():

  conn = FakeConnection(
    "POST /doge HTTP/1.0\r\n" + \
    "Content-Type: application/x-www-form-urlencoded\r\n\r\n" + \
    "firstname=Beautiful&lastname=Shibe")
  expected_return = u'HTTP/1.0 404 Not found\r\n' + \
          'Content-type: text/html\r\n' + \
          'Connection: close\r\n' + \
          '\r\n' + \
          'Invalid request'

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_bad_multipart_form_post():

  conn = FakeConnection(
    "POST /dingus HTTP/1.0\r\n" + \
    "Content-Type: multipart/form-data; boundary=AaB03x\r\n\r\n" +\
    "--AaB03x\r\n" +\
    "Content-Disposition: form-data; name='firstname'\r\n" +\
    "\r\n" +\
    "Beautiful\r\n" +\
    "--AaB03x\r\n" +\
    "Content-Disposition: form-data; name='lastname'\r\n" +\
    "\r\n" +\
    "Shibe\r\n" +\
    "--AaB03x\r\n" +\
    "Content-Disposition: form-data; name='files'; filename='file1.txt'\r\n" +\
    "Content-Type: text/plain\r\n" +\
    "\r\n" +\
    "... contents of file1.txt ...\r\n" +\
    "--AaB03x--\r\n"
    )
  expected_return = u'HTTP/1.0 404 Not found\r\n' + \
          'Content-type: text/html\r\n' + \
          'Connection: close\r\n' + \
          '\r\n' + \
          'Invalid request'

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_bad_page():

  conn = FakeConnection("GET /doge.html HTTP/1.0\r\n\r\n")
  expected_return = u'HTTP/1.0 404 Not found\r\n' + \
          'Content-type: text/html\r\n' + \
          'Connection: close\r\n' + \
          '\r\n' + \
          '<html><body>\n' +\
          '<h1>404 Error</h1>The page you requested was not found.\n' +\
          '</body></html>'

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

# Test a basic GET call.
def test_handle_connection_root():
  conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
  expected_return = u'HTTP/1.0 200 OK\r\n' + \
          'Content-type: text/html\r\n' + \
          '\r\n' + \
          '<html><body>\n' + \
          '<h1>Hello, world.</h1>This is zhopping\'s web server.\n' + \
          '<br/><a href="/form.html">Form (GET)</a>\n' + \
          '<br/><a href="/form_post.html">Form (POST)</a>\n' + \
          '<br/><a href="/content.html">Content</a>\n' + \
          '<br/><a href="/file.html">File</a>\n' + \
          '<br/><a href="/image.html">Image</a>\n' + \
          '</body></html>'

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_content():
  conn = FakeConnection("GET /content.html HTTP/1.0\r\n\r\n")
  expected_return = u'HTTP/1.0 200 OK\r\n' + \
          'Content-type: text/html\r\n' + \
          '\r\n' + \
          '<html><body><h1>Content</h1>This is a content.</body></html>'

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_file():
  conn = FakeConnection("GET /file.html HTTP/1.0\r\n\r\n")
  expected_return = u'HTTP/1.0 200 OK\r\n' + \
          'Content-type: text/html\r\n' + \
          '\r\n' + \
          '<html><body>\n<h1>File</h1>This is a file.\n</body></html>'

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)

def test_handle_connection_image():
  conn = FakeConnection("GET /image.html HTTP/1.0\r\n\r\n")
  expected_return = u'HTTP/1.0 200 OK\r\n' + \
          u'Content-type: text/html\r\n' + \
          u'\r\n' + \
          u'<html><body><h1>Image</h1><br>\n' + \
          '<img border="0" src="http://static3.wikia.nocookie.net/__cb20130826211346/creepypasta/images/0/01/DOGE.png" alt="DOGE">\n' + \
          '</body></html>'

  server.handle_connection(conn)

  assert conn.sent == expected_return, 'Expected:\n%s\n\nGot:\n%s' % (repr(expected_return),repr(conn.sent),)