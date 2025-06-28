# Git XL - A Git Extension for Excel

(Note: Git XL was previously called "git-xltrail")

Git XL is an open-source Git command line extension for managing Excel workbook files in Git.

The extension makes `git diff` work for Excel VBA (xls, xlt, xla, xlam, xlsx, xlsm, xlsb, xltx, xltm). Git XL does not require Excel as it works directly on the workbook file.

With Git XL installed, Git can diff Excel VBA just like any other source code file.

It is written in Python, with pre-compiled binaries available for Windows and macOS.

Installation instructions and docs are available at [https://www.xltrail.com/git-xl](https://www.xltrail.com/git-xl).


## Getting Started 

### Installation

#### Windows
You can install the Git XL client on Windows, using the pre-compiled binary installer.

#### macOS
For macOS, you can build from source using the provided scripts. See [BUILDING.md](BUILDING.md) for detailed instructions.

#### Build from Source
This repository can also be built-from-source using Python and PyInstaller on both Windows and macOS.

Git XL requires a global installation once per-machine. This can be done by
running:

```
C:\Developer>git xl install
```

Alternatively, initialise Git XL locally (per repository), using the --local option, inside the root folder of your repository’s local working copy:

```
C:\Developer>git xl install --local
```

### Usage

#### Diff workbooks

Get meaningful `git diff` output when comparing Excel workbook files containing VBA code.

```diff
C:\Developer>git diff dev..master
diff --xl a/Book1.xlsb b/Book1.xlsb
--- a/Book1.xlsb/VBA/Module/Module1
+++ b/Book1.xlsb/VBA/Module/Module1
@@ -1,4 +1,4 @@
 Option Explicit
 Public Function Version() As String
-   Version = "v1.0"
+   Version = "v1.1"
 End Function
```

## Docs

Docs are available at [https://www.xltrail.com/git-xl](https://www.xltrail.com/git-xl).


## Contributing

Please [open a new issue](https://github.com/xlwings/git-xl/issues) to report bugs or [create a pull request](https://github.com/xlwings/git-xl/pulls) to send patches.
