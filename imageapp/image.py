# image handling API
import sqlite3

class Image:
	def __init__(self, data, filetype, metadata):
		self.data = data
		self.metadata = metadata

		if (filetype == 'tif' or filetype == 'tiff'):
			self.filetype = 'tiff'
		elif (filetype == 'jpeg' or filetype == 'jpg'):
			self.filetype = 'jpg'
		else:
			self.filetype = filetype


def add_image(image):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	db.execute('INSERT INTO image_store (image, filetype, title, '
		'description, date_taken, location, comments) VALUES (?,?,?,?,?,?,?)', 
	(image.data, image.filetype, image.metadata['title'], image.metadata['description'], 
		image.metadata['date'], image.metadata['location'], ''))
	db.commit()
	db.close()

def add_comment(index, comment):
	comments = self.get_comments(index)
	comments_as_string = comments.join('::')
	commments = comments + '::' + comment
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	db.execute('UPDATE image_store SET comments=%s WHERE i=%s' % (comments, index), (comments))
	db.commit()
	db.close()

def add_comment_latest(comment):
	comments = self.get_latest_image_comments()
	comments_as_string = comments.join('::')
	commments = comments + '::' + comment
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	db.execute('UPDATE image_store SET comments=%s WHERE i=1' % (comments, index), (comments))
	db.commit()
	db.close()

def get_image(index):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT image, filetype, title, description, date_taken, location FROM image_store WHERE i=%s' % index)

	image, filetype, title, description, date_taken, location = c.fetchone()
	img = Image(image, filetype, {'title':title, 'description':description, 'location':location, 'date':date_taken})
	db.close()

	return img

# returns comments for a given image index as a list of strings
def get_comments(index):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT comments FROM image_store WHERE i=%s' % index)

	comments = c.fetchone()
	comments_as_list = comments.split('::')
	db.close()

	return comments_as_list

def get_latest_image_comments():
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT comments FROM image_store ORDER BY i DESC LIMIT 1')

	comments = c.fetchone()
	comments_as_list = comments.split('::')
	db.close()
	return comments_as_list

def num_images():
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT i FROM image_store ORDER BY i DESC')
	i = c.fetchone()
	db.close()
	if i is None:
		return 0
	return i[0]


def get_latest_image():
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	c.execute('SELECT image, filetype, title, description, date_taken, location FROM image_store ORDER BY i DESC LIMIT 1')

	image, filetype, title, description, date_taken, location = c.fetchone()
	img = Image(image, filetype, {'title':title, 'description':description, 'location':location, 'date':date_taken})
	db.close()
	return img

def matches_metadata(metadata, query):
	for value in metadata:
		if query in value:
			return True
	return False


def search_metadata(query):
	db = sqlite3.connect('images.sqlite')
	db.text_factory = bytes
	c = db.cursor()
	#returns matching rows in database as array of integers
	results = []
	c.execute('SELECT title, description, location FROM image_store ORDER BY i ASC')

	row = 0
	all_metadata = c.fetchall()
	for metadata in all_metadata:
		if matches_metadata(metadata, query):
			results.append(row)
		row += 1
	db.close()
	return results


