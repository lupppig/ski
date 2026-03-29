import os
from pathlib import Path
import subprocess


def run_python_file(working_directory, file_path, args=None):
	working_dir_abs = os.path.abspath(working_directory)
	norms_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
	validate_targ_dir = os.path.commonpath([working_dir_abs, norms_path]) == working_dir_abs

	if not validate_targ_dir:
		return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory' 
	
	path = Path(norms_path)
	if not  os.path.isfile(norms_path):
		return f'Error: "{file_path}" does not exist or is not a regular file'	

	if path.suffix != ".py":
		return f'Error: "{file_path}" is not a Python file'

	try:
		command = ["python3", norms_path]
		if args:
			command.extend(args)
		proc = subprocess.run(command, text=True, capture_output=True, timeout=30)

		if proc.returncode != 0:
			return f"Process exited with code {proc.returncode}"
		
		if not proc.stdout and not proc.stderr:
			return "No output produced"
		elif proc.stdout:
			return f"STDOUT: {proc.stdout}"
		else:
			return f"STDERR: {proc.stderr}"
	except Exception as e:
		return f"Error: executing Python file: {e}"


