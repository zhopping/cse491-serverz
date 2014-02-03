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

# Test a basic GET call.

def test_handle_connection_basic():
    conn = FakeConnection("GET / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<a href="/content">CONTENT</a><br>' + \
                      '<a href="/file">FILE</a><br>' + \
                      '<a href="/image">IMAGE</a><br>' + \
                      '<a href="/form">FORM</a><br>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_content():
    conn = FakeConnection("GET /content HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>' + \
                      'This is zhopping\'s Web server.'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /file HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>File</h1><br>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_file():
    conn = FakeConnection("GET /pagethatdoesntexist HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 404 Not Found\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Error 404 Page Not Found</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_image():
    conn = FakeConnection("GET /image HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Image Example</h1><br>' + \
                      '<img border="0" src="http://static3.wikia.nocookie.net/__' + \
                      'cb20130826211346/creepypasta/images/0/01/DOGE.png" alt="DOGE">'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_basic_form():
    conn = FakeConnection("GET /form HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      "<form action='/submit' method='POST'>" + \
                      "First Name: <input type='text' name='firstname'><br>" + \
                      "Last Name: <input type='text' name='lastname'><br>" + \
                      "<input type='submit' value='Submit'>" + \
                      "</form>"

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_handle_connection_post():
    conn = FakeConnection("POST / HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello, world.</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_form_submit_get():
    conn = FakeConnection("GET /submit?firstname=Dignitas&lastname=Imaqtpie HTTP/1.0\r\n\r\n")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello Mr. Dignitas Imaqtpie.</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)

def test_form_submit_post():
    conn = FakeConnection("POST /submit HTTP/1.0\r\n\r\nfirstname=Dignitas&lastname=Imaqtpie")
    expected_return = 'HTTP/1.0 200 OK\r\n' + \
                      'Content-type: text/html\r\n' + \
                      '\r\n' + \
                      '<h1>Hello Mr. Dignitas Imaqtpie.</h1>'

    server.handle_connection(conn)

    assert conn.sent == expected_return, 'Got: %s' % (repr(conn.sent),)
