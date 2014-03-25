# __init__.py is the top level file in a Python package.

from quixote.publish import Publisher

# this imports the class RootDirectory from the file 'root.py'
from .root import RootDirectory
from . import html, image

def create_publisher():
     p = Publisher(RootDirectory(), display_exceptions='plain')
     p.is_thread_safe = True
     return p
 
def setup():                            # stuff that should be run once.
    html.init_templates()

    some_data = open('imageapp/dice.png', 'rb').read()
    metadata = {'title':'Dice', 'description':'some dice', 'location':'Africa', 'date':'08/12/1999'}
    image.add_image(some_data, 'png', metadata)
    

def teardown():                         # stuff that should be run once.
    pass
