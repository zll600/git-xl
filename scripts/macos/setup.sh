#!/bin/bash

echo "Git XL - macOS Setup"
echo "==================="

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed. Please install uv first."
    echo "You can install it via: curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "Or via Homebrew: brew install uv"
    exit 1
fi

echo "uv version: $(uv --version)"

# Check if Python 3 is available (uv will handle this, but good to check)
if ! command -v python3 &> /dev/null; then
    echo "Warning: Python 3 not found in PATH. uv will manage Python for us."
fi

# Sync dependencies using uv
echo "Syncing dependencies with uv..."
uv sync

# Create icon if needed
if [ ! -f "scripts/macos/git-xl-logo.icns" ]; then
    echo "Creating macOS icon..."
    ./scripts/macos/create-icon.sh
fi

echo ""
echo "Setup complete!"
echo ""
echo "To build the application:"
echo "1. Run the build script: ./scripts/macos/build.sh"
echo ""
echo "To run tests:"
echo "1. uv run python -m pytest src/tests/"
echo ""
echo "To run commands in the uv environment:"
echo "1. uv run <command>" 