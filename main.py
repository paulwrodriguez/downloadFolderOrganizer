import os
import time
import ntpath
import threading
from pathlib import Path


def rename_file_helper(src_path, des_path, tries, max_tries, sleep_time):
    if tries >= max_tries:
        return
    tries = tries + 1

    try:
        os.rename(src_path, des_path)
        print("Moved ", src_path, " to ", des_path)
    except PermissionError as error:
        print("PermissionError - Thread: ", str(threading.get_native_id()))
        time.sleep(sleep_time)
        rename_file_helper(src_path, des_path, tries, max_tries, sleep_time)
    except FileNotFoundError as error:
        print("Another event must have moved the file because ", src_path, " does not exist")
    except FileExistsError as error:
        full_path_and_file_name, decimal, file_extension = des_path.rpartition(".")[:3]
        unique_file_name = "%s%s%s%s" % (full_path_and_file_name, "-1", decimal, file_extension)
        rename_file_helper(src_path, unique_file_name, tries, max_tries, sleep_time)  # possible infinite loop
    except Exception as error:
        print("Unexpected exception:", error)
        raise error


def rename_file(src_path, des_path):
    tries = 0
    max_tries = 5
    sleep_time = 5  # seconds
    rename_file_helper(src_path, des_path, tries, max_tries, sleep_time)


def mkdirs():
    os.makedirs(des + "\\txt", exist_ok=True)
    os.makedirs(des + "\\exe", exist_ok=True)
    os.makedirs(des + "\\pdf", exist_ok=True)
    os.makedirs(des + "\\zip", exist_ok=True)


def create_test_files(src):
    Path(src + '''\\text.txt''').touch()
    Path(src + '''\\pdf.pdf''').touch()
    Path(src + '''\\exe.exe''').touch()
    Path(src + '''\\zip.zip''').touch()


def process_file(filename):
    basename = ntpath.basename(filename)

    if filename.endswith('.txt'):
        new_name = des + '''\\txt\\''' + basename
    elif filename.endswith('.exe'):
        new_name = des + '''\\exe\\''' + basename
    elif filename.endswith('.pdf'):
        new_name = des + '''\\pdf\\''' + basename
    elif filename.endswith('.zip'):
        new_name = des + '''\\zip\\''' + basename
    else:
        return

    rename_file(src + '''\\''' + filename, new_name)


def handle_errors(src):
    previous_dir = os.getcwd();
    os.chdir(src)
    if len(os.listdir()) <= 0:
        print("Error: Could not find any files inside \'", src, "\' directory")
        exit(-1)
    os.chdir(previous_dir)


if __name__ == "__main__":
    src = "C:\\Users\\Paul\\Desktop\\Cerebro\\temp\\src\\downloads"
    des = "C:\\Users\\Paul\\Desktop\\Cerebro\\temp\\dest"

    mkdirs()  # create directories that will be supported
    # create_test_files(src)  # Make test files
    handle_errors(src)

    os.chdir(src)

    for filename in os.listdir():
        process_file(filename)  # send file to appropriate sub folder
