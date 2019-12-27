import os
import time
import ntpath
import threading
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

src = "C:\\Users\\Paul\\Desktop\\Cerebro\\temp\\src\\downloads"
des = "C:\\Users\\Paul\\Desktop\\Cerebro\\temp\\dest"


def on_deleted(event):
    print(f"what the f**k! Someone deleted {event.src_path}!")


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


def on_modified(event):
    print("event:", event.event_type, " src:", event.src_path)
    basename = ntpath.basename(event.src_path)

    if event.src_path.endswith('.txt'):
        new_name = des + '''\\txt\\''' + basename
    elif event.src_path.endswith('.exe'):
        new_name = des + '''\\exe\\''' + basename
    elif event.src_path.endswith('.pdf'):
        new_name = des + '''\\pdf\\''' + basename
    elif event.src_path.endswith('.zip'):
        new_name = des + '''\\zip\\''' + basename
    else:
        return

    rename_file(event.src_path, new_name)


def init():
    os.makedirs(des + "\\txt", exist_ok=True)
    os.makedirs(des + "\\exe", exist_ok=True)
    os.makedirs(des + "\\pdf", exist_ok=True)
    os.makedirs(des + "\\zip", exist_ok=True)


if __name__ == "__main__":
    init()
    patterns = "*"
    ignore_patterns = ""
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_modified
    # my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    # my_event_handler.on_moved = on_moved

    path = src
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, go_recursively)

    my_observer.start()
    print("Monitoring directory:", src)
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
