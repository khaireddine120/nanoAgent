import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):

    try:
        # Normalize both paths
        abs_working_directory = os.path.abspath(os.path.join(working_directory, directory))
        root_path = os.path.abspath(working_directory)

        # Validate directory boundaries
        if not abs_working_directory.startswith(root_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Validate that the path is a directory
        if not os.path.isdir(abs_working_directory):
            return f'Error: "{directory}" is not a directory'

        files_info = []
        summary_lines = []

        # Walk through directory (single loop handling both dirs and files)
        for root, dirs, files in os.walk(abs_working_directory):
            for name in dirs + files:
                path = os.path.join(root, name)
                try:
                    rel_path = os.path.relpath(path, abs_working_directory)
                    is_dir = os.path.isdir(path)
                    size = 0

                    if is_dir:
                        for dir_root, _, dir_files in os.walk(path):
                            for f in dir_files:
                                try:
                                    size += os.path.getsize(os.path.join(dir_root, f))
                                except Exception:
                                    pass
                    else:
                        size = os.path.getsize(path)

                    if not is_dir:
                        files_info.append({
                            "file_name": name,
                            "file_path": rel_path,
                            "size_bytes": size,
                            "last_modified": os.path.getmtime(path),
                        })

                    summary_lines.append(f"- {rel_path}: file_size={size} bytes, is_dir={is_dir}")

                except Exception as e:
                    return f"Error: Unable to access {path}: {e}"

        return "\n".join(summary_lines)

    except Exception as e:
        return f"Error: {e}"