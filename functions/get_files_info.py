import os

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        ret = f"Result for {"current" if directory == "." else directory} directory:\n"

        abs_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_path, directory))

        valid_target_dir = os.path.commonpath([abs_path, target_dir]) == abs_path
        if not valid_target_dir:
            return ret + f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return ret + f'Error: "{target_dir}" is not a directory'
        else:
            dirs_to_list = os.listdir(target_dir)
            formatted_paths: list[str] = list(map(lambda file_or_dir: f" - {file_or_dir}: file_size={os.path.getsize(target_dir + "/" + file_or_dir)} bytes, is_dir={"False" if not os.path.isdir(target_dir + "/" + file_or_dir) else "True"}", dirs_to_list))
            return ret + "\n".join(formatted_paths)
    except Exception as e:
        return f"\tError: {e}"
