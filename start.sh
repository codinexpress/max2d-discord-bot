#!/bin/sh

python3 -m venv .venv
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Check if requirements.txt exists and install if it does
# if [ -f "requirements.txt" ]; then
#   pip install -r requirements.txt
# fi

python main.py