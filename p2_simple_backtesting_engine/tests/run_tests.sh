#!/bin/bash
# run_test.sh

set -euo pipefail

# Optional first argument is the test file path, default to all tests
TEST_FILE="${1:-tests/}"

cd ..

# Run pytest
python -m pytest -v "$TEST_FILE"
