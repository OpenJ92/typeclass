#!/bin/bash

# Optional: activate virtual environment
# source venv/bin/activate

echo "Running unit tests..."

# Discover and run all unittests
python -m unittest discover -v -s typeclass/tests -p "*.py"

# Capture the exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "All tests passed!"
else
  echo "Some tests failed."
fi

exit $EXIT_CODE

