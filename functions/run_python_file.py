import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file within the working directory and returns its output. The file must have a .py extension.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the Python file relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="List of arguments to pass to the Python script.",
            ),
        },
        required=["file_path"],
    ),
)



def run_python_file(working_directory, file_path, args=[]):



    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    # Validate file boundaries
    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    if os.path.isdir(abs_file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    
    completed_process = ""
    try:
        result = subprocess.run(
            ["python3", abs_file_path] + args,
            capture_output=True,
            text=True,
            cwd=abs_working_dir,
            timeout=30
        )
        output = result.stdout
        error = result.stderr
        completed_process = "STDOUT: " + output + " STDERR: " + error
        if result.returncode != 0:
            completed_process = " Process exited with code " + str(result.returncode) + "\n" + completed_process

    except subprocess.TimeoutExpired:
        return "Error: Running file timed out"
    except Exception as e:
        return f"Error: Running file: {e}"

    if len(completed_process) > 0:
        return completed_process
    else:
        return "No output produced."
