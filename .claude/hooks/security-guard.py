#!/usr/bin/env python3
"""
Security Guard Hook for Claude Code.
Blocks dangerous bash commands before execution to prevent accidental data loss.

Blocked patterns:
- rm -rf / or rm -rf /* (recursive deletion from root)
- dd if=/dev/zero (destructive disk writes)
- mkfs (format filesystem)
- git reset --hard (destructive git reset)
- shutdown, reboot, halt (system shutdown)
- kill -9 (forceful process termination)
- : > (truncate important files)
- chmod 000 (permission removal)
"""

import json
import sys
import re


# List of dangerous command patterns
DANGEROUS_PATTERNS = [
    # Recursive deletion from root
    (r'rm\s+.*-rf\s+/?(\*|/)', 'Recursive deletion from root directory blocked'),
    (r'rm\s+.*-rf\s+~', 'Recursive deletion of home directory blocked'),

    # Destructive disk operations
    (r'dd\s+.*if=/dev/(zero|urandom|random)', 'Destructive disk write (dd) blocked'),
    (r'dd\s+.*of=/dev/\w+', 'Direct disk write (dd) blocked'),

    # Filesystem formatting
    (r'mkfs', 'Filesystem formatting command (mkfs) blocked'),
    (r'format\s+[A-Z]:', 'Windows format command blocked'),

    # System shutdown
    (r'shutdown\s+.*-h', 'System shutdown command blocked'),
    (r'reboot|halt|poweroff', 'System reboot/halt command blocked'),

    # Destructive git operations
    (r'git\s+reset\s+--hard', 'Destructive git reset blocked'),
    (r'git\s+push\s+.*--force', 'Forced git push blocked'),

    # Process termination
    (r'kill\s+-9', 'Force kill command (-9) blocked'),
    (r'killall\s+\w+', 'Kill all processes blocked'),

    # Permission removal
    (r'chmod\s+000', 'Permission removal (chmod 000) blocked'),
    (r'chmod\s+-R\s+000', 'Recursive permission removal blocked'),

    # Truncate files
    (r':\s*>\s*\S+', 'File truncation blocked'),
    (r'>\s*/etc/passwd', 'Modification of system files blocked'),
    (r'>\s*/etc/shadow', 'Modification of system files blocked'),

    # Fork bomb
    (r':\(\)\s*{\s*:\s*\|\s*:\s*&\s*};\s*:', 'Fork bomb detected and blocked'),
]

# Allowlist for safer variants
SAFE_PATTERNS = [
    r'rm\s+.*\.log',  # Remove log files (relatively safe)
    r'rm\s+.*\.tmp',  # Remove temp files (relatively safe)
    r'rm\s+-i\s+',    # Remove with interactive prompt (safer)
    r'git\s+reset\s+--soft',  # Soft reset (safe)
    r'git\s+reset\s+--mixed',  # Mixed reset (safe)
]


def check_dangerous_command(command: str) -> dict:
    """
    Check if a bash command is dangerous.

    Returns:
        dict: Empty dict if safe, blocking dict if dangerous
    """
    if not command or not command.strip():
        return {}

    # Check allowlist first
    for pattern in SAFE_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return {}  # Safe pattern found

    # Check dangerous patterns
    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE | re.MULTILINE):
            return {
                'continue': False,
                'stopReason': reason
            }

    return {}  # Command is safe


def main():
    """Main hook entry point."""
    try:
        # Read hook input from stdin
        hook_input = json.load(sys.stdin)

        # Extract bash command
        command = hook_input.get('tool_input', {}).get('command', '').strip()

        if not command:
            sys.exit(0)

        # Check if command is dangerous
        result = check_dangerous_command(command)

        # Output result as JSON
        if result:
            print(json.dumps(result))

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(json.dumps({
            'continue': False,
            'stopReason': f'Security check error: {str(e)}'
        }))


if __name__ == '__main__':
    main()
