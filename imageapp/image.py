# image handling API

images = {}

def add_image(data, filename, filetype, metadata):
    if images:
        image_num = max(images.keys()) + 1
    else:
        image_num = 0
        
    images[image_num] = [data, filename, filetype, metadata, ["This is a comment"]]
    return image_num

def get_image(num):
    return images[num]

def get_latest_image():
    image_num = max(images.keys())
    return images[image_num]

def get_image(index):
	if index in images.keys():
		return images[index]

def get_filenames():
	filenames = []
	for key in images.keys():
		filenames.append(images[key][1])
	return filenames
