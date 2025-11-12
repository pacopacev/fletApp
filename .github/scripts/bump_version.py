#!/usr/bin/env python3
"""Bump version script used by CI.
Writes src/version.py with APP_VERSION, MAJOR, MINOR, PATCH, BUILD_DATE, COMMIT_HASH and a formatted version string.
"""
import re
from datetime import datetime
import os
import subprocess


def main():
    version_path = os.path.join('src', 'version.py')

    # Read existing version if present
    current_version = '0.0.1'
    try:
        with open(version_path, 'r') as f:
            content = f.read()
        match = re.search(r"APP_VERSION\s*=\s*'([0-9]+\.[0-9]+\.[0-9]+)'", content)
        if match:
            current_version = match.group(1)
    except FileNotFoundError:
        pass

    print(f"Current version: {current_version}")

    # Bump patch
    major, minor, patch = map(int, current_version.split('.'))
    patch += 1
    new_version = f"{major}.{minor}.{patch}"

    print(f"New version: {new_version}")

    # Build metadata
    build_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    try:
        result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True)
        commit_hash = result.stdout.strip() or 'unknown'
    except Exception:
        commit_hash = 'unknown'

    version_content = f"""# Auto-generated version info
APP_VERSION = '{new_version}'
MAJOR = {major}
MINOR = {minor}
PATCH = {patch}
BUILD_DATE = '{build_date}'
COMMIT_HASH = '{commit_hash}'

# Version string in your desired format
version = f"V{{APP_VERSION}} Build: {{BUILD_DATE}}"
"""

    os.makedirs('src', exist_ok=True)
    with open(version_path, 'w') as f:
        f.write(version_content)

    # Print the value so the GitHub Actions step can capture it
    print(new_version)


if __name__ == '__main__':
    main()
