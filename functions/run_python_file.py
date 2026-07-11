import os
import subprocess


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