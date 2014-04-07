# image handling API

images = {}

def add_image(data, filetype, metadata):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = [data, filetype, metadata, ["This is a comment"]]
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]

def get_image(key):
	if key in images.keys():
		return images[key]

def get_keys():
	return images.keys()

def has_key(key):
	return key in images.keys()

def matches_metadata_search(key, query):
	metadata = images[key][2]
	for entry in metadata.keys():
		if query in metadata[entry]:
			return True
	return False

