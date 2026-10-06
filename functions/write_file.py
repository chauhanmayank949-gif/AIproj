

import os


schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write or overwrite a file with the specified content.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write."
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file."
                }
            },
            "required": ["file_path", "content"]
        }
    }
}


def write_file(
    working_directory: str,
    file_path: str,
    content: str
) -> str:
    try:
        working_path = os.path.abspath(working_directory)

        target_path = os.path.abspath(
            os.path.join(working_path, file_path)
        )

        if os.path.commonpath([working_path, target_path]) != working_path:
            return (
                f'Error: Cannot write to "{file_path}" '
                'as it is outside the permitted working directory'
            )

        if os.path.isdir(target_path):
            return (
                f'Error: Cannot write to "{file_path}" '
                'as it is a directory'
            )

        parent_dir = os.path.dirname(target_path)

        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" '
            f'({len(content)} characters written)'
        )

    except Exception as e:
        return f"Error: {e}"
