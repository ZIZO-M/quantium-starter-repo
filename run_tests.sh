#!/bin/bash

# Activate virtual environment
source venv/bin/activate

# Run test suite
python -m pytest test_app.py -v

# Capture pytest exit code and return it
if [ $? -eq 0 ]; then
    exit 0
else
    exit 1
fi
