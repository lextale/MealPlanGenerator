#!/bin/bash
set -e  # Exit if any command fails

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Working in: $SCRIPT_DIR"

echo "Cloning repositories..."
git clone https://github.com/noamgat/lm-format-enforcer.git

echo "Moving lmformatenforcer into thesisRepo/app..."
cp -r lm-format-enforcer/lmformatenforcer ./app/

echo "Cleaning up..."
rm -rf lm-format-enforcer

echo "Installing Python dependencies..."
pip install --no-deps -r requirements.txt
