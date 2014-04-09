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
    'filetype TEXT, title TEXT, description TEXT, location TEXT, date_taken TEXT, comments TEXT)')
    print "CREATING image_store TABLE"
    #db.execute('CREATE TABLE image_store (i INTEGER PRIMARY KEY, image BLOB, comments BLOB)');
    db.commit()
    db.close()
    html.init_templates()
    

def teardown():                         # stuff that should be run once.
    pass
