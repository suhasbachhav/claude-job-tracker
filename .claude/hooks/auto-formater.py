#!/usr/bin/env python3
"""
Auto-formatter hook for Claude Code.
Automatically formats files after Write/Edit operations based on file type.

Supported formats:
- JavaScript/TypeScript (prettier)
- Python (black)
- JSON (jq)
- YAML (yamllint)
- Markdown (prettier)
"""

import json
import sys
import subprocess
from pathlib import Path


def format_file(file_path: str) -> dict:
    """Format a file based on its type."""
    path = Path(file_path)

    if not path.exists():
        return {}

    suffix = path.suffix.lower()

    try:
        # JavaScript/TypeScript
        if suffix in ['.js', '.jsx', '.ts', '.tsx', '.mjs']:
            subprocess.run(['prettier', '--write', file_path],
                         capture_output=True, check=False)
            return {}

        # Python
        elif suffix == '.py':
            subprocess.run(['black', file_path],
                         capture_output=True, check=False)
            return {}

        # JSON
        elif suffix == '.json':
            result = subprocess.run(['jq', '--indent', '2', file_path],
                                  capture_output=True, text=True, check=False)
            if result.returncode == 0:
                Path(file_path).write_text(result.stdout)
            return {}

        # YAML
        elif suffix in ['.yaml', '.yml']:
            subprocess.run(['yamllint', '-d', 'relaxed', '-f', 'parsable', file_path],
                         capture_output=True, check=False)
            return {}

        # Markdown
        elif suffix == '.md':
            subprocess.run(['prettier', '--write', file_path],
                         capture_output=True, check=False)
            return {}

        # CSS/SCSS/LESS
        elif suffix in ['.css', '.scss', '.less']:
            subprocess.run(['prettier', '--write', file_path],
                         capture_output=True, check=False)
            return {}

        # HTML
        elif suffix in ['.html', '.htm']:
            subprocess.run(['prettier', '--write', file_path],
                         capture_output=True, check=False)
            return {}

        # Unsupported format
        else:
            return {}

    except Exception as e:
        return {
            'systemMessage': f'Formatting warning for {path.name}: {str(e)}'
        }


def main():
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        # Extract file path from tool input
        file_path = hook_input.get('tool_input', {}).get('file_path') or \
                   hook_input.get('tool_response', {}).get('filePath')

        if not file_path:
            sys.exit(0)

        # Format the file
        result = format_file(file_path)

        # Output result as JSON
        if result:
            print(json.dumps(result))

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(json.dumps({'systemMessage': f'Formatter error: {str(e)}'}))


if __name__ == '__main__':
    main()
