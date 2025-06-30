# Building Git XL

## Building on Windows

Using uv for dependency management is highly recommended.
Install dependencies via `uv sync`.

### Build the exe

From within the repository's root folder run

```
$ .\scripts\windows\build.bat
```

## Building on macOS

### Prerequisites

- Python 3.8 or higher (uv will manage this for you)
- uv (install via `curl -LsSf https://astral.sh/uv/install.sh | sh` or `brew install uv`)
- Git

### Setup and Build

1. **Run the setup script** (recommended):
   ```bash
   $ ./scripts/macos/setup.sh
   ```
   This will sync dependencies with uv and set up the icon.

2. **Manual setup** (alternative):
   ```bash
   # Sync dependencies with uv
   $ uv sync

   # Create icon
   $ ./scripts/macos/create-icon.sh
   ```

3. **Build the executables**:
   ```bash
   $ ./scripts/macos/build.sh
   ```

The built executables will be in the `dist/` folder:
- `git-xl-{arch}` (main CLI)
- `git-xl-diff-{arch}` (diff tool)

Where `{arch}` is either `arm64` (Apple Silicon) or `x86_64` (Intel).

### Running Tests

```bash
$ uv run python -m pytest src/tests/
```

### Running Commands in Development

```bash
$ uv run python src/cli.py --help
```
