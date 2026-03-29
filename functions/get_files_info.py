import os
from pathlib import Path



def get_files_info(working_directory, directory="."):
	working_directory_abs = os.path.abspath(working_directory)
	target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))

	validate_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs

	if not validate_target_dir:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	
	directory_path = Path(target_dir)
	if not directory_path.is_dir():
		return f'Error: "{directory}" is not a directory'

	output = []
	for item in directory_path.iterdir():
		name = item.name
		is_dir = item.is_dir()
		file_size = item.stat().st_size
		output.append(f"- {name}: file_size={file_size} bytes, is_dir={is_dir}")
	
	return "\n".join(output)

		


	