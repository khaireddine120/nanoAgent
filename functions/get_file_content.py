import os
from config import MAX_FILE_LENGTH
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a file within the working directory. Returns the file's text content, truncated if it exceeds a configured maximum length.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)


def get_file_content(working_directory, file_path):
    try:
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        root_path = os.path.abspath(working_directory)

        # Validate file boundaries
        if not abs_file_path.startswith(root_path):
            return f'Error: Cannot access "{file_path}" as it is outside the permitted working directory'

        # Validate that the path is a file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Truncate if longer than configured limit
        if len(content) > MAX_FILE_LENGTH:
            content = content[:MAX_FILE_LENGTH] + f'\n[...File "{file_path}" truncated at {MAX_FILE_LENGTH} characters]'

        return content

    except Exception as e:
        return f"Error: {e}"