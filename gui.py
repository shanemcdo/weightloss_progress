#!/usr/bin/env python3

import dotenv
import os
import tkinter as tk
from shared import getenv_mandatory, get_img
from PIL import ImageTk

def get_img_tk(dir_path: str, filename: str, scale: int = 8) -> ImageTk.PhotoImage:
	print(f'Loading "{filename}"')
	img = get_img(dir_path, filename)
	img = img.resize((img.width // scale, img.height // scale))
	return ImageTk.PhotoImage(img)

def run_gui(input_path: str, extension: str = 'JPG') -> int:
	root = tk.Tk()
	root.title('Weight Loss Progress')
	files = [
		get_img_tk(input_path, file)
		for file in sorted(os.listdir(input_path))
		if file.endswith('.' + extension)
	]
	if len(files) == 0:
		print(f'No files could be found in "{input_path}"')
		return 1
	left_index = 0
	right_index = len(files) - 1
	left = tk.Label(root, image = files[left_index])

	def left_prev():
		nonlocal left_index
		left_index -= 1
		if left_index < 0:
			left_index = 0
		left.config(image = files[left_index])

	def left_next():
		nonlocal left_index
		left_index += 1
		if left_index >= len(files):
			left_index = len(files) - 1
		left.config(image = files[left_index])

	def right_prev():
		nonlocal right_index
		right_index -= 1
		if right_index < 0:
			right_index = 0
		right.config(image = files[right_index])

	def right_next():
		nonlocal right_index
		right_index += 1
		if right_index >= len(files):
			right_index = len(files) - 1
		right.config(image = files[right_index])

	right = tk.Label(root, image = files[right_index])
	left_frame = tk.Frame(root)
	tk.Button(left_frame, text="Prev", command=left_prev).pack(side="left")
	tk.Button(left_frame, text="Next", command=left_next).pack(side="right")
	right_frame = tk.Frame(root)
	tk.Button(right_frame, text="Prev", command=right_prev).pack(side="left")
	tk.Button(right_frame, text="Next", command=right_next).pack(side="right")
	left.grid(column=0, row=0)
	right.grid(column=1, row=0)
	left_frame.grid(column=0, row=1)
	right_frame.grid(column=1, row=1)
	root.mainloop()
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
	return run_gui(input_path)

if __name__ == '__main__':
	exit(main())
