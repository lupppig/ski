import os
from pathlib import Path


def get_file_content(working_directory, file_path):
	working_dir_abs = os.path.abspath(working_directory)
	norms_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
	validate_targ_dir = os.path.commonpath([working_dir_abs, norms_path]) == working_dir_abs

	if not validate_targ_dir:
		return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
	
	file_path = Path(norms_path)
	if not file_path.is_file():
		return f'Error: File not found or is not a regular file: "{file_path}"'
	
	MAX_CHARS = 10_000
	content =  ""
	try:
		with open(norms_path,  'r') as file:
			content = file.read(MAX_CHARS)
			if file.read(1):
				content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
			file.seek(0)
		return content
	except Exception as e:
		return f'Error reading file "{file_path}": {str(e)}'
