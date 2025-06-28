# Building Git XL

## Building on Windows

Using a virtual environment is highly recommended. 
Install Python dependencies via `pip install -r requirements.txt`.

### Build the exe

From within the repository's root folder run

```
$ .\scripts\windows\build.bat
```

## Building on macOS

### Prerequisites

- Python 3.7 or higher
- pip3
- Git

### Setup and Build

1. **Run the setup script** (recommended):
   ```bash
   $ ./scripts/macos/setup.sh
   ```
   This will create a virtual environment, install dependencies, and set up the icon.

2. **Manual setup** (alternative):
   ```bash
   # Create virtual environment
   $ python3 -m venv venv
   $ source venv/bin/activate

   # Install dependencies
   $ pip install -r requirements.txt

   # Create icon
   $ ./scripts/macos/create-icon.sh
   ```

3. **Build the executables**:
   ```bash
   $ source venv/bin/activate  # if not already activated
   $ ./scripts/macos/build.sh
   ```

The built executables will be in the `dist/` folder:
- `git-xl-{arch}` (main CLI)
- `git-xl-diff-{arch}` (diff tool)

Where `{arch}` is either `arm64` (Apple Silicon) or `x86_64` (Intel).
