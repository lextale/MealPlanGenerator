#!/bin/bash
set -e  # Exit if any command fails

echo "Moving lmformatenforcer into thesisRepo/app..."
mv lm-format-enforcer/lmformatenforcer thesisRepo/app/

echo "Cleaning up..."
rm -rf lm-format-enforcer

echo "Installing Python dependencies..."
pip install --no-deps -r requirements.txt