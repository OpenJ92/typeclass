#!/usr/bin/env bash
set -e

# Save current directory
START_DIR="$(pwd)"

# Move to src where the package root lives
cd src || exit 1

# Run tests
python -m unittest discover -s typeclass/tests -v

# Return to original directory
cd "$START_DIR"
