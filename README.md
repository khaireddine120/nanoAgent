# nanoAgent

A lightweight AI agent framework for Google's Gemini AI with function calling capabilities. nanoAgent provides a minimal set of tools for file operations and Python script execution, enabling AI agents to interact with the file system in a controlled and secure manner.

## Features

- **File Operations**: Read, write, and list files within a working directory
- **Python Execution**: Run Python scripts with arguments and capture output
- **Security**: All operations are sandboxed to a specified working directory
- **Function Calling**: Built-in schema definitions for Google Gemini function calling
- **Example Application**: Includes a calculator CLI application as a demonstration

## Project Structure

```
nanoAgent/
├── functions/              # Core agent functions
│   ├── get_file_content.py    # Read file contents
│   ├── get_files_info.py      # List directory contents
│   ├── run_python_file.py     # Execute Python scripts
│   └── write_file.py          # Write to files
├── calculator/             # Example calculator application
│   ├── main.py                # CLI entry point
│   ├── pkg/
│   │   ├── calculator.py      # Calculator logic
│   │   └── render.py          # Output formatting
│   └── tests.py               # Unit tests
├── test_data/              # Test files
└── LICENSE                 # MIT License
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/khaireddine120/nanoAgent.git
cd nanoAgent
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install google-genai
```

## Core Functions

### 1. `get_file_content`
Reads the content of a file within the working directory.

**Parameters:**
- `file_path` (string): Path to the file relative to the working directory

**Features:**
- Validates file boundaries (prevents directory traversal)
- Truncates large files based on `MAX_FILE_LENGTH` configuration
- Returns error messages for invalid paths

### 2. `get_files_info`
Lists files in a directory with metadata.

**Parameters:**
- `directory` (string, optional): Directory to list (defaults to working directory)

**Returns:**
- File paths, sizes, and modification times
- Recursive directory size calculation

### 3. `run_python_file`
Executes a Python file and captures its output.

**Parameters:**
- `file_path` (string): Path to the Python file
- `args` (array, optional): Command-line arguments

**Features:**
- 30-second timeout protection
- Captures both stdout and stderr
- Returns exit codes for error handling

### 4. `write_file`
Writes content to a file, creating directories as needed.

**Parameters:**
- `file_path` (string): Target file path
- `content` (string): Content to write

**Features:**
- Automatic directory creation
- Overwrites existing files
- Validates file boundaries

## Calculator Example

The included calculator demonstrates a complete CLI application:

```bash
cd calculator
python main.py "3 + 5 * 2"
```

**Features:**
- Infix expression evaluation
- Operator precedence (+, -, *, /)
- JSON-formatted output
- Comprehensive error handling

**Example Output:**
```json
{
  "expression": "3 + 5 * 2",
  "result": 13.0
}
```

### Running Tests

```bash
cd calculator
python tests.py
```

## Usage with Google Gemini

The function schemas are designed for Google's Gemini AI function calling:

```python
from google.genai import types
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.write_file import schema_write_file, write_file

# Define tools for the AI agent
tools = [
    schema_get_file_content,
    schema_write_file,
    # ... other functions
]

# Use with Gemini API
# (Implementation depends on your specific use case)
```

## Security Considerations

All functions implement security measures:

- **Path Validation**: Prevents access outside the working directory
- **File Type Checking**: Validates file extensions and types
- **Timeout Protection**: Prevents infinite loops in script execution
- **Error Handling**: Graceful error messages without exposing system details

## Configuration

Create a `config.py` file to customize settings:

```python
# Maximum file length for reading (in characters)
MAX_FILE_LENGTH = 10000
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

**khairy** - [khaireddine120](https://github.com/khaireddine120)

## Acknowledgments

- Built for Google's Gemini AI function calling API
- Inspired by the need for lightweight, secure AI agent tools
