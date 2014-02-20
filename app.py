# from http://docs.python.org/2/library/wsgiref.html

import cgi
import jinja2
import traceback
import urllib
from StringIO import StringIO
from urlparse import urlparse, parse_qs
from wsgiref.simple_server import make_server

def render_page(page, params):
    loader = jinja2.FileSystemLoader('./templates')
    env = jinja2.Environment(loader=loader)
    template = env.get_template(page)
    rendered_page = template.render(params).encode('latin-1', 'replace')
    return str(rendered_page)


class MyApp(object):
    def __call__(self, environ, start_response):
        options = {'/'            : 'index',
                   '/content'     : 'content',
                   '/files'       : 'files',
                   '/images'      : 'images',
                   '/form'        : 'form',
                   '/submit'      : 'submit'   }

        path = environ['PATH_INFO']
        page = options.get(path)

        return self.retrieve_page(environ, start_response, page)

    def retrieve_page(self, environ, start_response, page):
    	if page is None:
    		start_response('404 Not Found', [('Content-type', 'text/html')])
    		page = 'error'
        elif page is 'images':
            return self.serve_image(start_response)
        elif page is 'files':
            return self.serve_text_file(start_response)
        elif page is 'submit':
            return self.submit(environ, start_response)
    	else:
    		start_response('200 OK', [('Content-type', 'text/html')])
    	page_filename = '%s.html' % page
    	return render_page(page_filename,'')

    def submit(self, environ, start_response):
        method = environ['REQUEST_METHOD']
        if method == 'GET':
            return self.handle_get(environ, start_response)
        else:
            return self.handle_post(environ, start_response)

    def handle_get(self, environ, start_response):
        start_response('200 OK', [('Content-type', 'text/html')])
        params = parse_qs(environ['QUERY_STRING'])
        return render_page('submit.html', params)

    def handle_post(self, environ, start_response):
        con_type = environ['CONTENT_TYPE']
        headers = {}
        params ={} 
        for k, v in environ.iteritems():
            headers['content-type'] = environ['CONTENT_TYPE']
            headers['content-length'] = environ['CONTENT_LENGTH']
            fs = cgi.FieldStorage(fp=environ['wsgi.input'], \
                                  headers=headers, environ=environ)
            params.update({x: [fs[x].value] for x in fs.keys()}) 
        start_response('200 OK', [('Content-type', 'text/html')])
        print params
        return render_page('submit.html', params)

    def serve_text_file(self, start_response):
        start_response('200 OK', [('Content-type', 'text/plain')])
        fp = open('./text_file.txt', "rb")
        data = fp.read()
        fp.close()
        return data

    def serve_image(self, start_response):
        start_response('200 OK', [('Content-type', 'image/jpeg')])
        fp = open('./doge.jpg', "rb")
        data = fp.read()
        fp.close()
        return data

def make_app():
    return MyApp()
