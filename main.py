#!/usr/bin/env python3

import dotenv
import os
from PIL import Image
from shared import find_oldest_photo, getenv_mandatory, get_img

def generate_progress_photo(input_path: str, output_path: str, extension: str = 'JPG') -> int:
	'''
	find the oldest and most recent photo in the input directory and creates a new image placing both photos next to eachother
	:input_path: the path to the directory to look for input files
		the expected filename for these photos are YYYYMMDDBW###.#.JPG
	:output_path: the path to the directory to write output files
		the output filename will be YYYYMMDDtoYYYYMMDD.JPG
	:extension: the file extension to look for in input_path and use for output
	:return: code passed to main; 1 for failure 0 for success
	'''
	oldest_name = find_oldest_photo(input_path, extension)
	newest_name = find_oldest_photo(input_path, extension, reverse = True)
	oldest_date = oldest_name[:8]
	newest_date = newest_name[:8]
	output_name = f'{oldest_date}to{newest_date}.{extension}'
	output_fullpath = os.path.join(output_path, output_name)
	oldest_img = get_img(os.path.join(input_path, oldest_name), oldest_date)
	newest_img = get_img(os.path.join(input_path, newest_name), newest_date)
	assert oldest_img.mode == newest_img.mode
	assert oldest_img.height == newest_img.height
	output_img = Image.new(oldest_img.mode, (oldest_img.width * 2, oldest_img.height))
	output_img.paste(oldest_img, (0, 0))
	output_img.paste(newest_img, (oldest_img.width, 0))
	output_img.save(output_fullpath)
	return 0

def generate_progress_gif(input_path: str, output_path: str, extension: str = 'JPG') -> int:
	'''
	Create a gif of all the photos in order
	:input_path: the path to the directory to look for input files
		the expected filename for these photos are YYYYMMDDBW###.#.JPG
	:output_path: the path to the directory to write output files
		the output filename will be YYYYMMDDtoYYYYMMDD.gif
	:extension: the file extension to look for in input_path
	:return: code passed to main; 1 for failure 0 for success
	'''
	oldest_name = find_oldest_photo(input_path, extension)
	newest_name = find_oldest_photo(input_path, extension, reverse = True)
	oldest_date = oldest_name[:8]
	newest_date = newest_name[:8]
	output_name = f'{oldest_date}to{newest_date}.gif'
	output_fullpath = os.path.join(output_path, output_name)
	imgs = [ get_img(os.path.join(input_path, file), file[:8]) for file in sorted(os.listdir(input_path)) if file.endswith('.' + extension) ]
	if len(imgs) == 0:
		print(f'No images found in "{input_path}" for gif')
		return 1
	imgs[0].save(
		output_fullpath,
		append_images = imgs[1:],
		save_all = True,
		duration = 500,
		loop = 0,
	)
	return 0

def main() -> int:
	'''
	Driver code
	:return: code passed to exit; 1 for failure 0 for success
	'''
	dotenv.load_dotenv()
	input_path = getenv_mandatory('INPUT_PATH')
	if not os.path.isdir(input_path):
		print(f'input_path = "{input_path}" not valid directory')
		return 1
	output_path = getenv_mandatory('OUTPUT_PATH')
	if not os.path.isdir(output_path):
		print(f'output_path = "{output_path}" not valid directory')
		return 1
	return generate_progress_photo(input_path, output_path) # or generate_progress_gif(input_path, output_path)

if __name__ == '__main__':
	exit(main())
