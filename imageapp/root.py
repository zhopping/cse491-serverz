import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

class RootDirectory(Directory):
    _q_exports = []
    key = 0

    @export(name='')                    # this makes it public.
    def index(self):
        metadata = image.get_latest_image()[2]

        return html.render('index.html', values=metadata)

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()
        print request.form.keys()

        the_file = request.form['file']
        filetype = the_file.orig_filename.split('.')[1]
        filename = the_file.orig_filename
        if (filetype == 'tif' or filetype == 'tiff'):
            filetype = 'tiff'
        elif filetype == 'jpeg' or filetype == 'jpg':
            filetype = 'jpg'
        print 'received file of type: ' + filetype
        print dir(the_file)
        print 'received file with name:', the_file.base_filename
        data = the_file.read(int(1e9))

        # Get metadata from form
        title = request.form['title']
        description = request.form['description']
        location = request.form['location']
        date = request.form['date']
        metadata = {'title':title, 'description':description, 'location':location, 'date':date}

        image.add_image(data, filetype, metadata)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        metadata = image.get_latest_image()[2]

        return html.render('image.html', values = metadata)

    @export(name='thumbnails')
    def thumbnails(self):
        keys = image.get_keys()
        data = {'keys':keys}

        return html.render('thumbnails.html', values = data)

    @export(name='thumbnail')
    def thumbnail(self):
        print "GETTING THUMB"
        if not image.has_key(self.key):
            self.key = 0
            return
        response = quixote.get_response()
        img = image.get_image(self.key)
        self.key += 1
        response.set_content_type('image/%s' % img[1])
        
        return img[0]

    @export(name='image_raw')
    def image_raw(self):
        response = quixote.get_response()
        img = image.get_latest_image()
        response.set_content_type('image/%s' % img[1])
        
        return img[0]

    @export(name='comments')
    def comments_raw(self):
        # TODO: send comments data
        reponse = quixote.get_response()
        response.set_content_type('text/html')
        return

    @export(name='search')
    def search(self):
        request = quixote.get_request()
        query = request.form['query']
        for key in image.get_keys():
            if image.matches_metadata_search(key, query):
                response = quixote.get_response()
                img = image.get_image(key)
                response.set_content_type('image/%s' % img[1])
        
                return img[0]


    @export(name='search_result')
    def search_result(self):
        pass


