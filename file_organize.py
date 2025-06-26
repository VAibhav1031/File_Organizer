import os
import shutil


def organize_file(folder_path: str):
    if not os.path.isdir(folder_path):
        print("❌ It is  not  a folder/directory ")
        return

    files = os.listdir(folder_path)

    FILE_TYPES = {
        "Pictures": [".png", "jpeg", "jpg", "webp"],
        "Videos": [".mov", ".mkv", ".mp4"],
        "Documents": [".pdf", ".md", ".txt" or ".text", ".epub", ".docx", ".csv"],
    }

    for file in files:
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            moved = False

            for folder, extension in FILE_TYPES.items():
                if ext in extension:
                    target_dir = os.path.join(folder_path, folder)
                    os.makedirs(target_dir, exist_ok=True)
                    shutil.move(file_path, target_dir)
                    moved = True
                    break

            if not moved:
                others_dir = os.path.join(folder_path, "Others")
                os.makedirs(others_dir, exist_ok=True)
                shutil.move(file_path, os.path.join(others_dir, file))

    print("✅ Organizing complete.")


def dry_run(folder_path: str):
    if not os.path.isdir(folder_path):
        print("❌ It is  not  a folder/directory ")
        return

    forbidden_paths = ["/", "/home", "/boot", "/etc", "/usr", "/bin"]
    if (
        os.path.abspath(folder_path) in forbidden_paths
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

        print("❌ Dangerous directory. Aborting.")
        return

    print("DRY RUN MODE:")
    files = os.listdir(folder_path)

    FILE_TYPES = {
        "Pictures": [".png", "jpeg", "jpg", "webp"],
        "Videos": [".mov", ".mkv", ".mp4"],
        "Documents": [".pdf", ".md", ".txt", ".text", ".epub", ".docx", ".csv"],
    }

    for file in files:
        file_path = os.path.join(folder_path, file)

        if (
            file.startswith(".")
            or file.lower().endswith(".db")
            or file in [".DS_Store", "Thumbs.db"]
        ):
            continue

        if os.path.isfile(file_path):
            _, ext = os.path.splitext(file)
            ext = ext.lower()

            moved = False

            for folder, extension in FILE_TYPES.items():
                if ext in extension:
                    target_dir = os.path.join(folder_path, folder)
                    chk = (
                        "Directory already there "
                        if os.path.isdir(target_dir)
                        else f"we are creating the folder '{folder}/' "
                    )
                    print(chk)
                    print(f"Moving '{file}'  to  the  {folder}")
                    moved = True
                    break

            if not moved:
                others_dir = os.path.join(folder_path, "Others")
                chk = (
                    "Directory already there "
                    if os.path.isdir(others_dir)
                    else "we are creating the folder 'Others/' "
                )
                print(chk)
                print(f"Moving '{file}'  to  the  'Others/' ")

    print("✅ Dry Run completed, Check the process .")


if __name__ == "__main__":
    target = input("Enter absolute file  path:").strip()
    dry_run(target)
