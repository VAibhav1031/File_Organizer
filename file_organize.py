import os
import shutil
import sys
from log_config import setup_logging
import logging


logger = logging.getLogger("organizer")

FILE_TYPES = {
    "Pictures": [".png", ".jpeg", ".jpg", ".webp"],
    "Videos": [".mov", ".mkv", ".mp4"],
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


def organize_file(folder_path: str):
    if not os.path.isdir(folder_path):
        logger.warning("❌ It is  not  a folder/directory ")
        return

    if not forbidden_path(folder_path):
        return
    files = os.listdir(folder_path)

    logger.info(f"📂 Starting organization in '{folder_path}'...")
    for file in files:
        logger.debug(f"Processing file: {file}")
        if (
            file.startswith(".")
            or file.lower().endswith((".db", ".ini"))
            or file.lower() in [".DS_Store", "Thumbs.db", "desktop.ini"]
            or file in FILE_TYPES.keys()
            and os.path.isdir(os.path.join(folder_path, file))
        ):
            logger.warning("Skipping hidden/system file")
            continue
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
                        moved = True
                        break
                    except Exception as e:
                        logger.error(f"Error: {e}")

            if not moved:
                others_dir = os.path.join(folder_path, "Others")
                os.makedirs(others_dir, exist_ok=True)
                try:
                    shutil.move(file_path, os.path.join(others_dir, file))
                except Exception as e:
                    logger.error(f"Error : {e}")

    logger.info("✅ Organizing complete.")


def dry_run(folder_path: str):
    if not forbidden_path(folder_path):
        return

    logger.info("DRY RUN MODE:")
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
            and os.path.isdir(os.path.join(folder_path, file))
        ):
            continue

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
                chk_msg = f"Directory '{destination_folder_name}/' already exists."
            else:
                chk_msg = f"We would create the folder '{destination_folder_name}/'."
                would_be_created_folders.add(
                    destination_folder_name
                )  # Mark it as "would be created"

            logger.debug(chk_msg)
            logger.info(f"Moving '{file}' to the '{destination_folder_name}/'")

    logger.debug("✅ Dry Run completed, Check the process .")


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv
    log_to_file = "--logfile" in sys.argv
    quiet = "--quiet" in sys.argv
    setup_logging(verbose=verbose, quiet=quiet, log_to_file=log_to_file)
    if len(sys.argv) < 2:
        print("Usage: python file_organize.py <command> [args...]")
        print("command: ")
        print("dry_run: IT is  used  to dry run all movements")
        print("organize: IT is  used to  organize  files according to their type")
        print("  --help, -h : Show this help message.")
        sys.exit(1)

    command = sys.argv[1].lower()
    if command in ("--help", "--h"):
        print("Usage: python file_organize.py <command> [args...]")
        print("Commands: ")
        print("dry_run      : Stimulates the file Organization in specified folder")
        print("organize: Organizeed the file in specified folder")
        print("--help, -h   : Show this help message.")
        sys.exit(0)

    folder_path_arg = None
    if len(sys.argv) >= 3:
        folder_path_arg = sys.argv[2]
    target_folder = folder_path_arg

    if target_folder is None:
        print(f"No Folder path has been given for the {command}")
        target_folder = input("Enter the absoulte folder path: ").strip()
        if not target_folder:
            print("ABORTING, Exiting")
            sys.exit(1)

    if not os.path.isdir(target_folder):
        print("❌ It is  not  a folder/directory ")
        sys.exit(1)

    if command == "dry_run":
        dry_run(target_folder)

    elif command == "organize":
        print(
            "WARNING: This will reorganize the files. This process is irreversible (you can do manually but for big)"
        )

        confirm = input("Are you sure (YES/NO): ")
        if confirm.lower() == "yes":
            organize_file(target_folder)
        else:
            print("Operation Cancelled")
            sys.exit(0)

    else:
        print(f"❌ Error: Unkown command {command}")
        print("Use: python organize_file.py --help or --h, for usage instruction")
        sys.exit(0)
