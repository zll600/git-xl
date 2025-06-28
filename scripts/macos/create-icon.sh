#!/bin/bash

# Create icns icon from the Windows ico file
# This script uses the built-in sips command available on macOS

ICO_FILE="scripts/windows/git-xl-logo.ico"
ICNS_FILE="scripts/macos/git-xl-logo.icns"

if [ ! -f "$ICO_FILE" ]; then
    echo "Error: Source icon file not found: $ICO_FILE"
    exit 1
fi

echo "Converting $ICO_FILE to $ICNS_FILE..."

# Use sips to convert ico to icns
sips -s format icns "$ICO_FILE" --out "$ICNS_FILE"

if [ $? -eq 0 ]; then
    echo "Icon conversion successful: $ICNS_FILE"
else
    echo "Error: Icon conversion failed"
    exit 1
fi 