

import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute a Python file with optional arguments.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute."
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Optional arguments to pass to the Python file."
                }
            },
            "required": ["file_path"]
        }
    }
}


def run_python_file(
    working_directory: str,
    file_path: str,
    args: list[str] | None = None
) -> str:
    try:
        working_path = os.path.abspath(working_directory)

        target_path = os.path.abspath(
            os.path.join(working_path, file_path)
        )

        if os.path.commonpath([working_path, target_path]) != working_path:
            return (
                f'Error: Cannot execute "{file_path}" '
                'as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_path):
            return (
                f'Error: "{file_path}" '
                'does not exist or is not a regular file'
            )

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_path]

        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        output_parts = []

        if result.returncode != 0:
            output_parts.append(
                f"Process exited with code {result.returncode}"
            )

        if result.stdout:
            output_parts.append(
                f"STDOUT:\n{result.stdout}"
            )

        if result.stderr:
            output_parts.append(
                f"STDERR:\n{result.stderr}"
            )

        if not output_parts:
            output_parts.append("No output produced")

        return "\n".join(output_parts)

    except subprocess.TimeoutExpired:
        return "Error: Python file execution timed out after 30 seconds"

    except Exception as e:
        return f"Error: executing Python file: {e}"
