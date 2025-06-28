#!/bin/bash

echo "Git XL - macOS Setup"
echo "==================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    echo "You can install it via Homebrew: brew install python3"
    exit 1
fi

echo "Python version: $(python3 --version)"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not available. Please install pip3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create icon if needed
if [ ! -f "scripts/macos/git-xl-logo.icns" ]; then
    echo "Creating macOS icon..."
    ./scripts/macos/create-icon.sh
fi

echo ""
echo "Setup complete!"
echo ""
echo "To build the application:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the build script: ./scripts/macos/build.sh"
echo ""
echo "To run tests:"
echo "1. python -m pytest src/tests/" 