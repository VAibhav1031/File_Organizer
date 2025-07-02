import os
import shutil
import sys
from shelvr.log_config import setup_logging
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


# for semantic purpose when  we  used  to get the  pictures/ in os.listdir  and there is  Pictures/
# in FILE_TYPES.keys() ,  so it will make mistake there

CATEGORY_FOLDERS = set(folder.lower() for folder in FILE_TYPES)


def color_level(level, text):
    colors = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "DEBUG": Fore.CYAN,
    }
    return colors.get(level, "") + text + Style.RESET_ALL


def forbidden_path(folder_path):
    if os.path.abspath(folder_path) in FORBIDDEN_PATHS:
        # os.path.abspath is  very important we cant directlly comapre the  folder_path to the FORBIDDEN_PATHS
        # Sometime they dont like forbidden_path cause they are in absoulte states that why it can cause problem
        # like
        # "."  --> acts as Current working directory path
        # ///user/  --> it is still /user/
        # /../.. -->  this is imporatn like   when we use ../ it is reverseing back one director
        # so os.path.abspath() helps in this  it may no check if direcotry  is valid but follow rule
        logger.warning("❌ Dangerous directory. Aborting.")
        return False
    return True


def confirm_prompt(msg, depth):
    indent = "  " * depth
    return input(
        f"{indent}{Fore.YELLOW}{msg} [Y/n]: {Style.RESET_ALL}"
    ).strip().lower() in ["", "y", "yes"]


def _process_directory(folder_path, recursive, depth):
    if not forbidden_path(folder_path):
        return

    try:
        files = os.listdir(folder_path)
    except OSError as e:
        logger.error(f"Could not  able  to access {folder_path}: {e}")
        return

    for file in files:
        file_path = os.path.join(folder_path, file)
        logger.debug(f"Processing file: {file}")

        if (
            file.startswith(".")
            or file.lower().endswith((".db", ".ini"))
            or file.lower() in [".DS_Store", "Thumbs.db", "desktop.ini"]
            or file.lower() in CATEGORY_FOLDERS
        ):
            logger.debug("Skipping hidden/system file")
            continue

        if os.path.isdir(file_path) and recursive:
            if confirm_prompt(f"⚠️ Enter folder: '{file_path}'?", depth):
                yield from _process_directory(file_path, recursive, depth + 1)
            continue
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            destination_folder = "Others"
            for folder, extensions in FILE_TYPES.items():
                if ext in extensions:
                    destination_folder = folder
                    break

            yield file, file_path, destination_folder


def organize_file(folder_path, recursive=False, depth=0):
    logger.info(f"📂 Starting organization in '{folder_path}'...")
    file_moved = 0

    for file, file_path, destination_folder in _process_directory(
        folder_path, recursive, depth
    ):
        target_dir = os.path.join(folder_path, destination_folder)
        try:
            os.makedirs(target_dir, exist_ok=True)
            shutil.move(file_path, target_dir)
            logger.info(f"Moved: '{file}' -> {destination_folder}/")
            file_moved += 1

        except shutil.Error as e:
            logger.error(f"Error in moving the files : {e}")
        except OSError as e:
            logger.error(f"Error in creating the directory/folder :{e}")

    if depth == 0:
        logger.info(f"Organizing completed, Total files moved {file_moved}")


def dry_run(folder_path: str, recursive=False, depth=0):
    logger.info(f"📁 DRY RUN: {Fore.CYAN}{folder_path}{Style.RESET_ALL}")

    try:
        would_be_created_folders = {
            d
            for d in os.listdir(folder_path)
            if os.path.isdir(os.path.join(folder_path, d))
        }
    except OSError as e:
        logger.error(f"Could not access '{folder_path}': {e}")
        return

    for file, _, destination_folder in _process_directory(
        folder_path, recursive, depth
    ):
        if destination_folder not in would_be_created_folders:
            logger.debug(f"Would create folder: '{destination_folder}/'")
            would_be_created_folders.add(destination_folder)
        else:
            logger.debug(f"Folder exists: '{destination_folder}/'")

        logger.info(f"Would move: '{file}' -> {destination_folder}/")

    if depth == 0:
        logger.info("✅ Dry Run completed.")


def main():
    parser = argparse.ArgumentParser(
        description="File Organizer CLI",
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
    group.add_argument("--quiet", "-q", action="store_true",
                       help="Suppress Output")

    parser.add_argument("--logfile", action="store_true",
                        help="Log to file as well")
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
    setup_logging(verbose=args.verbose, quiet=args.quiet,
                  log_to_file=args.logfile)

    if not os.path.isdir(args.path):
        logger.warning("❌ Provided path is not a directory")
        sys.exit(1)

    if args.command == "dry_run":
        dry_run(args.path, args.recursive)
    elif args.command == "organize":
        print(
            f"{
                Fore.RED
            }⚠️ WARNING: This will move files. It cannot be undone automatically.{
                Style.RESET_ALL
            }"
        )
        if input(
            f"{Fore.YELLOW}Continue? [Y/n]: {Style.RESET_ALL}"
        ).strip().lower() in ["", "y", "yes"]:
            organize_file(args.path, args.recursive)
        else:
            print(f"{Fore.RED}Operation Cancelled{Style.RESET_ALL}")
            sys.exit(0)
