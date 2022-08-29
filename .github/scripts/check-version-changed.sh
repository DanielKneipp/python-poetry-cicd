#!/usr/bin/env bash

# About the fail-fast flags: https://gist.github.com/mohanpedala/1e2ff5661761d3abd0385e8223e16425
set -e
set -o pipefail

git show master:pyproject.toml > pyproject-master.toml

current_version=$(python .github/scripts/get-version.py pyproject.toml)
master_version=$(python .github/scripts/get-version.py pyproject-master.toml)

rm pyproject-master.toml

if [[ ${current_version} == "" || ${master_version} == "" ]]; then
    >&2 echo "Current version (${current_version}) or master version (${master_version}) empty"
    exit 1
fi

if [[ ${current_version} == ${master_version} ]]; then
    >&2 echo "Versions must change from ${current_version}"
    exit 1
fi

echo "Current version: $current_version"
echo "master version: $master_version"
