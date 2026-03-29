import os
from pathlib import Path



def write_file(working_directory, file_path, content):
	working_dir_abs = os.path.abspath(working_directory)
	norms_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
	validate_targ_dir = os.path.commonpath([working_dir_abs, norms_path]) == working_dir_abs

	if not validate_targ_dir:
		return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
	
	file_path = Path(norms_path)
	if  file_path.is_dir():
		return f'Error: Cannot write to "{file_path}" as it is a directory'
	os.makedirs(working_dir_abs, exist_ok=True)


	try:
		n = 0
		with open(norms_path, 'w') as f:
			n = f.write(content)
		return f'Successfully wrote to "{file_path}" ({n} characters written)'
	except Exception as e:
		return f'Failed to write to {file_path} with exception {e}'
	