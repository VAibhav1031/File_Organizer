import os
import shutil
import sys
from log_config import setup_logging
import logging
import argparse


# __name__ if  you have  bigger application having different modules and all
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
    if (
        os.path.abspath(folder_path) in FORBIDDEN_PATHS
    ):  # os.path.abspath() helps  in following absolute path convention , it doesnt gurante path authentacity ,
        # for example . it is a current working directory it could be home also anything ,
        # same (../) or (../../) will be  a directory excluding current one from it  so
        # we dont know that path may look ok  but it could be the one of the forbidden_path
        # clear :::
        # os.path.abspath(".")        # ➝ "/home/vaibhav/Projects"
        # os.path.abspath("../")      # ➝ "/home/vaibhav"
        # os.path.abspath("/etc")     # ➝ "/etc" (unchanged, already absolute)
        # os.path.abspath("////usr")  # ➝ "/usr"
        #
        # so we cant  directly match the folder_path to the forbidden_paths could be ther absoulte version is
        # DANGEROUSSSSS

        logger.warning("❌ Dangerous directory. Aborting.")
        return False
    return True


def organize_file(folder_path, depth, recursive=False):
    if not forbidden_path(folder_path):
        return
    files = os.listdir(folder_path)

    logger.info(f"📂 Starting organization in '{folder_path}'...")
    file_moved = 0
    for file in files:
        logger.debug(f"Processing file: {file}")
        if (
            file.startswith(".")
            or file.lower().endswith((".db", ".ini"))
            or file.lower() in [".DS_Store", "Thumbs.db", "desktop.ini"]
            or file in FILE_TYPES.keys()
            or (os.path.isdir(os.path.join(folder_path, file)) and not recursive)
        ):
            logger.warning("Skipping hidden/system file")
            continue

        if os.path.isdir(os.path.join(folder_path, file)) and recursive:
            indent = " " * depth
            print(
                f"{indent}⚠️ Folder '{
                    os.path.join(folder_path, file)
                }' looks like an application or nested structure."
            )
            confirm = (
                input("Do you want to organize this folder too? yes/no: ")
                .strip()
                .lower()
            )
            if confirm != "yes":
                continue
            organize_file(
                os.path.join(folder_path, file),
                depth + 1,
                recursive=recursive,
            )

        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            moved = False

            for folder, extension in FILE_TYPES.items():
                if ext in extension:
                    target_dir = os.path.join(folder_path, folder)
                    os.makedirs(target_dir, exist_ok=True)
                    try:
                        shutil.move(file_path, target_dir)
                        file_moved += 1
                        moved = True
                        break
                    except Exception as e:
                        logger.error(f"Error: {e}")

            if not moved:
                others_dir = os.path.join(folder_path, "Others")
                os.makedirs(others_dir, exist_ok=True)
                try:
                    shutil.move(file_path, os.path.join(others_dir, file))
                    file_moved += 1
                except Exception as e:
                    logger.error(f"Error : {e}")
    if depth == 0:
        logger.info(f"✅ Organizing complete. Total file moved {file_moved}")


def dry_run(folder_path: str, depth, recursive=False):
    if not forbidden_path(folder_path):
        return

    print("\n")
    logger.info(f"DRY RUN MODE {folder_path}:\n")
    files = os.listdir(folder_path)
    # Keep track of folders that *would be* created during this dry run
    # Initialize with existing subdirectories of the target folder
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
            or (os.path.isdir(os.path.join(folder_path, file)) and not recursive)
        ):
            continue

        if os.path.isdir(os.path.join(folder_path, file)) and recursive:
            indent = " " * depth
            print(
                f"{indent}⚠️ Folder '{
                    os.path.join(folder_path, file)
                }' looks like an application or nested structure."
            )
            confirm = (
                input("Do you want to organize this folder too? yes/no").strip().lower()
            )
            if confirm != "yes":
                continue
            dry_run(
                os.path.join(folder_path, file),
                depth + 1,
                recursive=recursive,
            )

        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            destination_folder_name = "Others"  # Default to Others

            for folder_type, extensions_list in FILE_TYPES.items():
                if ext in extensions_list:
                    destination_folder_name = folder_type
                    break

            # Now, check if this folder *would be* created or already exists
            if destination_folder_name in would_be_created_folders:
                chk_msg = f"Directory '{
                    destination_folder_name}/' already exists."
            else:
                chk_msg = f"We would create the folder '{
                    destination_folder_name}/'."
                would_be_created_folders.add(
                    destination_folder_name
                )  # Mark it as "would be created"

            logger.debug(chk_msg)
            logger.info(f"Moving '{file}' to the '{destination_folder_name}/'")

    if depth == 0:
        logger.info("✅ Dry Run completed, Check the process .")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This  is  File Organizer CLI ",
        epilog="Example: python organize.py organize ~/Downloads --verbose",
    )
    parser.add_argument(
        "command",
        choices=["dry_run", "organize"],
        help="Choose what action to perform ",
    )
    parser.add_argument("path", help="Target folder path to organize ")

    # grouping the conflicting optional arguments like --verbose and --quiet which can cause problem together
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--verbose", "-v", action="store_true", help=" Enable Verbose Output"
    )
    group.add_argument("--quiet", "-q", action="store_true",
                       help="Supress Output")

    parser.add_argument(
        "--logfile", action="store_true", help="Log to file instead of just console"
    )

    parser.add_argument(
        "--recursive", action="store_true", help="Also organize files in subdirectories"
    )

    # this  we  are gonnnnnna  use  to make the version of  the cli
    parser.add_argument(
        "--version",
        action="version",
        version="File Organizer CLI version 1.0.0",
        help="Show program's version number and exit",
    )

    args = parser.parse_args()

    setup_logging(verbose=args.verbose, quiet=args.quiet,
                  log_to_file=args.logfile)
    command = args.command
    target_folder = args.path
    if not os.path.isdir(target_folder):
        logger.warning("❌ It is  not  a folder/directory ")
        sys.exit(1)

    if command == "dry_run":
        dry_run(target_folder, 0, args.recursive)

    elif command == "organize":
        print(
            "WARNING: This will reorganize the files. This process is irreversible (you can do manually but for big)"
        )

        confirm = input("Are you sure (YES/NO): ")
        if confirm.lower() == "yes":
            organize_file(target_folder, 0, args.recursive)
        else:
            print("Operation Cancelled")
            sys.exit(0)

    else:
        print(f"❌ Error: Unkown command {command}")
        logger.warning(f"User entered unknown command: {command}")
        print("Use: python organize_file.py --help or --h, for usage instruction")
        sys.exit(1)
