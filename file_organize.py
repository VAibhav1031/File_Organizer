import os
import shutil
import sys
from log_config import setup_logging
import logging
import argparse
from colorama import Fore, Style, init

init(autoreset=True)

logger = logging.getLogger("organizer")

FILE_TYPES = {
    "Pictures": [".png", ".jpeg", ".jpg", ".webp"],
    "Videos": [".mov", ".mkv", ".mp4", ".gif"],
    "Documents": [".pdf", ".md", ".txt", ".text", ".epub", ".docx", ".csv"],
    "Archives": [".zip", ".tar", ".gz", ".rar"],
    "Executables": [".exe", ".sh", ".run", ".appimage"],
    "Code": [
        ".py",
        ".js",
        ".html",
        ".css",
        ".java",
        ".c",
        ".cpp",
        ".h",
        ".go",
        ".rs",
    ],
}

FORBIDDEN_PATHS = [
    os.path.abspath("/"),
    os.path.abspath("/home"),
    os.path.abspath("/boot"),
    os.path.abspath("/etc"),
    os.path.abspath("/usr"),
    os.path.abspath("/bin"),
    os.path.abspath(os.path.expanduser("~")),
]


def forbidden_path(folder_path):
    if os.path.abspath(folder_path) in FORBIDDEN_PATHS:
        logger.warning(Fore.RED + "❌ Dangerous directory. Aborting.")
        return False
    return True


def confirm_prompt(msg, depth):
    indent = "  " * depth
    return input(
        Fore.YELLOW + f"{indent}{msg} [Y/n]: " + Style.RESET_ALL
    ).strip().lower() in ["", "y", "yes"]


def organize_file(folder_path, depth, recursive=False):
    if not forbidden_path(folder_path):
        return
    files = os.listdir(folder_path)

    logger.info(Fore.CYAN + f"📂 Starting organization in '{folder_path}'...")
    file_moved = 0
    for file in files:
        file_path = os.path.join(folder_path, file)
        logger.debug(f"Processing file: {file}")

        if (
            file.startswith(".")
            or file.lower().endswith((".db", ".ini"))
            or file.lower() in [".DS_Store", "Thumbs.db", "desktop.ini"]
            or file in FILE_TYPES.keys()
            or (os.path.isdir(file_path) and not recursive)
        ):
            logger.debug("Skipping hidden/system file")
            continue

        if os.path.isdir(file_path) and recursive:
            if confirm_prompt(f"⚠️ Enter folder: '{file_path}'?", depth):
                organize_file(file_path, depth + 1, recursive=recursive)
            continue

        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            moved = False
            for folder, extensions in FILE_TYPES.items():
                if ext in extensions:
                    target_dir = os.path.join(folder_path, folder)
                    os.makedirs(target_dir, exist_ok=True)
                    try:
                        shutil.move(file_path, target_dir)
                        file_moved += 1
                        moved = True
                        break
                    except Exception as e:
                        logger.error(Fore.RED + f"Error: {e}")

            if not moved:
                others_dir = os.path.join(folder_path, "Others")
                os.makedirs(others_dir, exist_ok=True)
                try:
                    shutil.move(file_path, os.path.join(others_dir, file))
                    file_moved += 1
                except Exception as e:
                    logger.error(Fore.RED + f"Error : {e}")

    if depth == 0:
        logger.info(
            Fore.GREEN + f"✅ Organizing complete. Total file moved {file_moved}"
        )


def dry_run(folder_path: str, depth, recursive=False):
    if not forbidden_path(folder_path):
        return

    print(Fore.CYAN + f"\n📁 DRY RUN: {folder_path}\n")
    files = os.listdir(folder_path)

    would_be_created_folders = {
        d
        for d in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, d))
    }

    for file in files:
        file_path = os.path.join(folder_path, file)

        if (
            file.startswith(".")
            or file.lower().endswith((".db", ".ini"))
            or file.lower() in [".DS_Store", "Thumbs.db", "desktop.ini"]
            or file in FILE_TYPES.keys()
            or (os.path.isdir(file_path) and not recursive)
        ):
            continue

        if os.path.isdir(file_path) and recursive:
            if confirm_prompt(f"⚠️ Enter folder: '{file_path}'?", depth):
                dry_run(file_path, depth + 1, recursive=recursive)
            continue

        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            destination_folder = "Others"
            for folder_type, extensions in FILE_TYPES.items():
                if ext in extensions:
                    destination_folder = folder_type
                    break

            if destination_folder not in would_be_created_folders:
                logger.debug(f"Would create folder: '{destination_folder}/'")
                would_be_created_folders.add(destination_folder)
            else:
                logger.debug(f"Folder exists: '{destination_folder}/'")

            logger.info(Fore.YELLOW + f"Would move: '{file}' → {destination_folder}/")

    if depth == 0:
        logger.info(Fore.GREEN + "✅ Dry Run completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="📦 File Organizer CLI",
        epilog="Example: python organize.py organize ~/Downloads --verbose",
    )
    parser.add_argument(
        "command", choices=["dry_run", "organize"], help="Action to perform"
    )
    parser.add_argument("path", help="Target folder path to organize")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--verbose", "-v", action="store_true", help="Enable Verbose Output"
    )
    group.add_argument("--quiet", "-q", action="store_true", help="Suppress Output")

    parser.add_argument("--logfile", action="store_true", help="Log to file as well")
    parser.add_argument(
        "--recursive", action="store_true", help="Organize subdirectories too"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="File Organizer CLI v1.0.0",
        help="Show version and exit",
    )

    args = parser.parse_args()
    setup_logging(verbose=args.verbose, quiet=args.quiet, log_to_file=args.logfile)

    if not os.path.isdir(args.path):
        logger.warning(Fore.RED + "❌ Provided path is not a directory")
        sys.exit(1)

    if args.command == "dry_run":
        dry_run(args.path, 0, args.recursive)
    elif args.command == "organize":
        print(
            Fore.RED
            + "⚠️ WARNING: This will move files. It cannot be undone automatically."
        )
        if input(
            Fore.YELLOW + "Continue? [Y/n]: " + Style.RESET_ALL
        ).strip().lower() in ["", "y", "yes"]:
            organize_file(args.path, 0, args.recursive)
        else:
            print("Operation Cancelled")
            sys.exit(0)
