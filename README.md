# 🌳 SHELVR — Smart File Organizer CLI

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub](https://img.shields.io/badge/GitHub-VAibhav1031%2Fshelvr-blue)](https://github.com/VAibhav1031/shelvr)
[![Status](https://img.shields.io/badge/status-active-brightgreen.svg)](https://github.com/VAibhav1031/shelvr)

A safe, extensible command-line tool for organizing files by type with support for dry runs, recursive operations, and comprehensive logging.

## 🚀 Quick Start

```bash
# Install from PyPI
pip install shelvr

# Organize your Downloads folder
shelvr organize ~/Downloads --recursive --verbose

# Preview changes without moving files
shelvr dry-run ~/Desktop --verbose
```

## ✨ Features

- **🗂️ Smart Organization**: Automatically categorizes files into folders by type
- **🔍 Dry Run Mode**: Preview changes before executing
- **📁 Recursive Processing**: Handle subdirectories with `--recursive`
- **📊 Flexible Logging**: Console and file logging with verbosity control
- **🔒 Safety First**: Built-in path validation to prevent system-wide accidents
- **🔧 Extensible**: Easy to add custom file types and organization logic
- **⚡ Fast & Lightweight**: Minimal dependencies, maximum performance

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install shelvr
```

### From Source
```bash
git clone https://github.com/VAibhav1031/shelvr.git
cd shelvr
pip install -e .
```

### Development Install
```bash
git clone https://github.com/VAibhav1031/shelvr.git
cd shelvr
pip install -e ".[dev]"
```

## 🛠️ Usage

### Basic Commands

```bash
# Organize files in current directory
shelvr organize .

# Organize with recursive subdirectory processing
shelvr organize ~/Downloads --recursive

# Dry run to preview changes
shelvr dry-run ~/Desktop --verbose

# Save logs to file
shelvr organize ~/Documents --logfile --verbose
```

### Command Reference

| Command | Description |
|---------|-------------|
| `organize` | Move files to organized folders |
| `dry-run` | Preview organization without moving files |

### Options

| Option | Short | Description |
|--------|-------|-------------|
| `--recursive` | `-r` | Process subdirectories recursively |
| `--verbose` | `-v` | Enable verbose logging |
| `--quiet` | `-q` | Suppress non-essential output |
| `--logfile` | `-l` | Save logs to `organize.log` |
| `--version` | | Show version information |
| `--help` | `-h` | Show help message |

## 📋 File Type Categories

SHELVR organizes files into these default categories:

| Category | Extensions |
|----------|------------|
| **Documents** | `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt` |
| **Images** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`, `.webp` |
| **Videos** | `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`, `.flv`, `.webm` |
| **Audio** | `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`, `.wma` |
| **Archives** | `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2` |
| **Code** | `.py`, `.js`, `.html`, `.css`, `.java`, `.cpp`, `.c` |


## 📊 Examples

### Organize Downloads Folder
```bash
shelvr organize ~/Downloads --recursive --verbose
```

### Preview Organization
```bash
shelvr dry-run ~/Desktop --verbose
# Output:
# [DRY RUN] Would move: document.pdf → Documents/document.pdf
# [DRY RUN] Would move: image.jpg → Images/image.jpg
# [DRY RUN] Would move: video.mp4 → Videos/video.mp4
```

### Quiet Mode with Logging
```bash
shelvr organize ~/Documents --quiet --logfile
```

## 🛣️ Roadmap

- [ ] **Undo Operations**: Reverse previous organizations
- [ ] **Batch Processing**: Handle multiple directories
- [ ] **TUI Interface**: Terminal-based user interface
- [ ] **Custom Rules**: Advanced file organization rules
- [ ] **Cloud Integration**: Support for cloud storage
- [ ] **Performance Improvements**: Faster processing for large directories

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


<div align="center">
  <strong>Made with ❤️ by developers, for developers</strong>
</div>
