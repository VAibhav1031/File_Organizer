# 🌳 SHELVR — File Organizer CLI

`shelvr` is a safe, extensible command-line tool written in Python for organizing files by type. 
It supports recursive operations, dry runs, logging, and CLI flags for customizable behavior.
Currently adding undo , batches and many other features also so keep following 

-----

## ✨ Features

  * Organizes files into folders by type (e.g., `Pictures`, `Documents`, `Videos`, etc.)
  * **Dry run mode** (preview changes without moving files)
  * **Recursive subdirectory processing** (`--recursive`)
  * **Verbosity control** (`--verbose`, `--quiet`)
  * **Console + file logging**
  * **Safe path checks** to prevent accidental system-wide changes
  * **Easily extensible** (add custom file types or logic)

-----

## 📦 Installation

Once published on PyPI:

```bash
pip install shelvr
```

Or install locally:

```bash
git clone https://github.com/your-username/tidy-tree.git
cd shelvr
pip install .
```

-----

## 🚀 Usage

```bash
shelvr organize ~/Downloads --recursive --verbose
shelvr dry_run ~/Desktop --logfile
```

### Available Commands

  * `organize`: Actually move files
  * `dry_run`: Preview what would happen

### Options

  * `--recursive`: Organize subdirectories
  * `--verbose` / `--quiet`: Set log level
  * `--logfile`: Save logs to `organize.log`
  * `--version`: Show version info

-----

## 🛠 Ongoing Development

  * Recursive support (`--recursive`)
  * Moved from `sys.argv` to `argparse`
  * Logging to both console and file
  * Packaged and ready for PyPI
  * Basic unit tests (planned)
