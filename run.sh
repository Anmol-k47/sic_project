#!/bin/bash
echo "============================================"
echo "  WorkMatch Pro v3 — Quick Start (Linux/Mac)"
echo "============================================"
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not found. Install it first."
    exit 1
fi

# Create virtual env if not exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Download spaCy model
python -m spacy download en_core_web_sm -q 2>/dev/null

# Run the app
echo ""
echo "Starting WorkMatch Pro v3..."
echo ""
python app.py
