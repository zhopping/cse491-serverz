import quixote
from quixote.directory import Directory, export, subdir

from . import html, image, accountmanager
from image import Image
from accountmanager import Account

class RootDirectory(Directory):
    _q_exports = []

    @export(name='')                    # this makes it public.
    def index(self):
        data = image.get_latest_image().metadata
        comments = image.get_latest_image_comments()
        data['image_comments'] = comments
        current_user = quixote.get_request().get_cookie('user')
        if (current_user is not None):
            data['user'] = current_user
        return html.render('index.html', values=data)

    @export(name='upload')
    def upload(self):
        current_user = quixote.get_request().get_cookie('user')
        if (current_user is not None):
            data['user'] = current_user
        return html.render('upload.html')

    @export(name='create_account')
    def create_account(self):
        request = quixote.get_request()
        user = request.form['username']
        password = request.form['password']
        account = Account(user, password)
        if accountmanager.exists_username(user):
            return self.account_name_taken()
        accountmanager.add_account(account)
        quixote.get_response().set_cookie('user', user, path='/')
        return quixote.redirect('./')

    @export(name='account_name_taken')
    def account_name_taken(self):
        return html.render('account_name_taken.html')

    @export(name='invalid_login')
    def invalid_login(self):
        return html.render('invalid_login.html')

    @export(name='login')
    def login(self):
        request = quixote.get_request()
        user = request.form['username']
        password = request.form['password']
        account = Account(user, password)
        if accountmanager.is_valid_login(account):
            response = quixote.get_response()
            response.set_cookie('user', user, path='/')
            return quixote.redirect('./')
        return self.invalid_login()

    @export(name='logout')
    def logout(self):
        quixote.get_response().expire_cookie('user', path='/')
        return quixote.redirect('./')

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
        key = request.form['key']
        data = image.get_image(key).metadata
        comments = image.get_comments(key)
        data['image_comments'] = comments
        current_user = quixote.get_request().get_cookie('user')
        if (current_user is not None):
            data['user'] = current_user

        return html.render('image.html', values = data)

    @export(name='image_with_key')
    def image_with_key(self):
        request = quixote.get_request()
        key = request.form['key']
        data = image.get_image(key).metadata
        data['key'] = key
        data['image_comments'] = image.get_comments(key)
        current_user = quixote.get_request().get_cookie('user')
        if (current_user is not None):
            data['user'] = current_user

        return html.render('image_with_key.html', values = data)

    @export(name='image_latest')
    def image_latest(self):
        data = image.get_latest_image().metadata
        data['image_comments'] = image.get_latest_image_comments()
        current_user = quixote.get_request().get_cookie('user')
        if (current_user is not None):
            data['user'] = current_user

        return html.render('image.html', values = data)

    @export(name='image_raw_latest')
    def image_raw_latest(self):
        response = quixote.get_response()
        img = image.get_latest_image()
        response.set_content_type('image/%s' % img.filetype)
        
        return img.data

    @export(name='thumbnails')
    def thumbnails(self):
        num_images = image.num_images()
        data = {'image_keys':[i+1 for i in range(num_images)]}
        current_user = quixote.get_request().get_cookie('user')
        if (current_user is not None):
            data['user'] = current_user

        return html.render('thumbnails.html', values = data)

    @export(name='image_raw')
    def image_raw(self):
        request = quixote.get_request()
        key = request.form['key']
        response = quixote.get_response()
        img = image.get_image(key)
        response.set_content_type('image/%s' % img.filetype)
        
        return img.data

    @export(name='add_comment')
    def add_comment(self):
        request = quixote.get_request()
        key = request.form['key']
        comment = request.form['comment']
        image.add_comment_at_index(key, comment)
        return quixote.redirect('./image_with_key?key=%s' % key)

    @export(name="add_comment_latest")
    def add_comment_latest(self):
        request = quixote.get_request()
        comment = request.form['comment']
        image.add_comment_to_latest_upload(comment)
        return quixote.redirect('./')

    @export(name='search_results')
    def search_results(self):
        request = quixote.get_request()
        query = request.form['query']
        data = {'image_keys':image.search_metadata(query)}
        current_user = quixote.get_request().get_cookie('user')
        if (current_user is not None):
            data['user'] = current_user

        return html.render('search_results.html', values = data)
