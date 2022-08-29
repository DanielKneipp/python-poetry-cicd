import sys
import toml

pyproject_file_name = sys.argv[1]


pyproject_file_content = toml.load(pyproject_file_name)

version = pyproject_file_content.get("tool", {}).get("poetry", {}).get("version", "")

if version:
    print(version)
else:
    print(f"version field not found on file {pyproject_file_name}", file=sys.stderr)
    exit(1)
