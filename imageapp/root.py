import quixote
from quixote.directory import Directory, export, subdir

from . import html, image

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        metadata = image.get_latest_image().metadata

        return html.render('index.html', values=metadata)

    @export(name='upload')
    def upload(self):
        return html.render('upload.html')

    @export(name='upload_receive')
    def upload_receive(self):
        request = quixote.get_request()

        the_file = request.form['file']
        filetype = the_file.orig_filename.split('.')[1]
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
        img = Image(data, filetype, metadata)
        image.add_image(img)

        return quixote.redirect('./')

    @export(name='image')
    def image(self):
        request = quixote.get_request()
        key = request.form[key]
        metadata = image.get_image(key).metadata

        return html.render('image.html', values = metadata)

    @export(name='image')
    def image_latest(self):
        metadata = image.get_latest_image().metadata

        return html.render('image.html', values = metadata)

    @export(name='thumbnails')
    def thumbnails(self):
        num_images = image.num_images
        data = {'image_keys':[i for i in range(num_images)]}

        return html.render('thumbnails.html', values = data)

    @export(name='image_raw')
    def image_raw(self):
        request = quixote.get_request()
        key = request.form[key]
        response = quixote.get_response()
        img = image.get_image(key)
        response.set_content_type('image/%s' % img.filetype)
        
        return img.data

    @export(name='comments')
    def comments(self):
        request = quixote.get_request()
        key = request.form[key]
        response = quixote.get_response()
        coms = image.get_comments(key)
        return 'COMMENT LOL DOGE'


    @export(name='search_results')
    def search_results(self):
        request = quixote.get_request()
        query = request.form[query]
        data = {'image_keys':image.search_metadata(query)}

        return html.render('search_results.html', values = data)


