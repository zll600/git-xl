#!/bin/bash

# Determine Python architecture
PYTHON_ARCH=$(uv run python -c "import platform; print(platform.machine())")

echo "Building for architecture: $PYTHON_ARCH"

# Update version info
uv run python ./scripts/macos/update-version-info.py

# Clean any previous builds
rm -rf build dist *.spec

# Build the diff executable
uv run pyinstaller --onefile --clean ./src/diff.py --name="git-xl-diff-$PYTHON_ARCH" --icon ./scripts/macos/git-xl-logo.icns

# Build the main CLI executable  
uv run pyinstaller --onefile --clean ./src/cli.py --name="git-xl-$PYTHON_ARCH" --icon ./scripts/macos/git-xl-logo.icns

echo "Build complete. Executables created:"
echo "- dist/git-xl-diff-$PYTHON_ARCH"
echo "- dist/git-xl-$PYTHON_ARCH" 