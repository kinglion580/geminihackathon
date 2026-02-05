#!/bin/bash

# Quick Start Script for Confidence Calibration Demo

echo "╔════════════════════════════════════════════════════════════╗"
echo "║  Confidence Calibration System - Quick Start Demo         ║"
echo "║  EU AI Act Compliant                                       ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "════════════════════════════════════════════════════════════"
echo "Running Demo..."
echo "════════════════════════════════════════════════════════════"
echo ""

# Run demo
python examples/demo.py

echo ""
echo "════════════════════════════════════════════════════════════"
echo "Demo completed!"
echo ""
echo "To run tests:"
echo "  python tests/test_calibration.py"
echo ""
echo "To start API server:"
echo "  python -m api.app"
echo "  Then visit: http://localhost:8000/docs"
echo "════════════════════════════════════════════════════════════"
