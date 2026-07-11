import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs or executes a python file in a path relative to the working directory using the python command. Returns the STDOUT and STDERR of said python file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path of python .py file to run, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": { "type": "string" },
                    "description": "Arguments to pass to the Python program that is going to be run, if any"
                },
            },
            "required": ["file_path"],
        },
    },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_file = os.path.commonpath([abs_path, target_file]) == abs_path

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        process = subprocess.run(command, cwd=abs_path, capture_output=True, check=True, text=True, timeout=30)

        output: str = ""
        if process.returncode != 0:
            output += f"Process exited with code {process.returncode}\n"
        #if no output
        if not process.stdout and not process.stderr:
            output += f"No output produced\n"
        else:
            output += f"STDOUT: {process.stdout if process.stdout else "No output"}\nSTDERR: {process.stderr if process.stderr else "No output"}\n"
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"