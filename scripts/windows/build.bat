@ECHO OFF
uv run python -c "import sys;print('x64' if sys.maxsize > 2**32 else 'x86')" > PYTHON_ARCH
set /p PYTHON_ARCH= < PYTHON_ARCH
del PYTHON_ARCH

uv run python .\scripts\windows\update-version-info.py
uv run pyinstaller --onefile .\src\diff.py --name=git-xl-diff-%PYTHON_ARCH%.exe --version-file .\scripts\windows\git-xl-version-info.py --icon .\scripts\windows\git-xl-logo.ico
uv run pyinstaller --onefile .\src\cli.py --name=git-xl-%PYTHON_ARCH%.exe --version-file .\scripts\windows\git-xl-version-info.py --icon .\scripts\windows\git-xl-logo.ico
