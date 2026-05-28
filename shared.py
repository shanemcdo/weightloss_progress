import os
from PIL import Image, ImageDraw, ImageFont

def find_oldest_photo(path: str, extension: str, reverse: bool = False) -> str:
	'''
	find the oldest file based on the date in the filename.
	This assumes all files require the
	:path: the path to the directory to look
	:extension: the extension of the filenames to look through
	:reverse: False by default, if True return newest photo
	'''
	files = sorted(
		(file for file in os.listdir(path) if file.endswith('.' + extension)),
		reverse = reverse
	)
	if len(files) == 0:
		print(f'No valid viles found in "{path}"')
		exit(1)
	return files[0]

def getenv_mandatory(key: str) -> str:
	'''
	get an environment variable and exit the program with failure if not found.
	'''
	result = os.getenv(key)
	if result is None:
		print(f'Mandatory key "{key}" not found in .env')
		exit(1)
	return result

def get_img(path: str, label: str) -> Image.Image:
	'''
	Get image and add label to top left
	:path: path to image to open
	:label: label to add to top left of image
	'''
	img = Image.open(path)
	img = img.transpose(Image.Transpose.ROTATE_270) # for some reason iphone photos need to be rotated
	font = ImageFont.load_default(150)
	draw = ImageDraw.Draw(img)
	draw.text((10, 10), label, 0, font)
	return img


