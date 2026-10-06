

import os


schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read the contents of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read."
                }
            },
            "required": ["file_path"]
        }
    }
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir = os.path.abspath(working_directory)

        target_path = os.path.abspath(
            os.path.join(working_dir, file_path)
        )

        if os.path.commonpath([working_dir, target_path]) != working_dir:
            return (
                f'Error: Cannot read "{file_path}" '
                'as it is outside the permitted working directory'
            )

        if not os.path.isfile(target_path):
            return (
                f'Error: "{file_path}" '
                'does not exist or is not a regular file'
            )

        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()

        if len(content) > 10000:
            return (
                content[:10000]
                + "\n[...File content truncated at 10000 characters...]"
            )

        return content

    except Exception as e:
        return f"Error: {e}"
