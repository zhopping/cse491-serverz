# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher
import os.path

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image
from image import Image
import sqlite3

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    db = sqlite3.connect('images.sqlite')
    c = db.cursor()
    c.execute('CREATE TABLE if not exists image_store (i INTEGER PRIMARY KEY, image BLOB,' +
    'filetype TEXT, title TEXT, description TEXT, location TEXT, date_taken TEXT, comments TEXT,'
    'owner TEXT)')
    c.execute('CREATE TABLE if not exists account_store (i INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    print "NUM IMAGES IN DB:"
    print image.num_images()
    if image.num_images() < 1:
        print "ADDING DEFAULT DICE IMG"
        some_data = open('imageapp/dice.png', 'rb').read()
        metadata = {'title':'Dice', 'description':'some dice', 'location':'Diceville', 'date':'08/12/1999'}
        image.add_image(Image(some_data, 'png', metadata), '')
    
    db.commit()
    db.close()
    html.init_templates()
    

def teardown():                         # stuff that should be run once.
    pass
