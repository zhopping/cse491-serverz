# image handling API
import sqlite3

db = sqlite3.connect('images.sqlite')
# configure to retrieve bytes, not text
db.text_factory = bytes
c = db.cursor()

class Image:
	def __init__(self, data, filetype, metadata):
		self.data = data
		if (filetype == 'tif' or filetype == 'tiff'):
            self.filetype = 'tiff'
        elif filetype == 'jpeg' or filetype == 'jpg':
            self.filetype = 'jpg'
        else:
        	self.filetype = filetype
		self.metadata = metadata


def add_image(image): 
    db.execute('INSERT INTO image_store (image) VALUES (?)', (image,))
	db.commit()

def get_image(index):
	c.execute('SELECT image FROM image_store WHERE i=%s' % index)

	i,image = c.fetchone()

	return image

def num_images():
	c.execute('SELECT i FROM image_store')
	return c.rowcount


def get_latest_image():
	c.execute('SELECT image FROM image_store ORDER BY i DESC LIMIT 1')
	image = c.fetchone()
	return image

def matches_metadata(metadata, query):
	for value in metadata.itervalues():
		if query in value:
			return True
	return False


def search_metadata(query):
	#returns matching rows in database as array of integers
	results = []
	c.execute('SELECT image FROM image_store ORDER BY i ASC')

	row = 0
	all_images = c.fetchall()
	for (image in all_images):
		if matches_metadata(image.metadata, query):
			results.append(row)
		row += 1
	return results


