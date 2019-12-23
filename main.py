import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def handle_event(event):
    print("inside the handle event")


if __name__ == "__main__":
    print("inside main")
    pattern = "*"
    ignorePatter = ""
    ignoreDirectory = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(pattern,ignorePatter, ignoreDirectory, case_sensitive)

    my_event_handler.on_any_event(handle_event)
    my_event_handler.on_created(handle_event)
    my_event_handler.on_modified(handle_event)
    my_event_handler.on_moved(handle_event)

    path = "."
    go_recursive = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursive)

    my_observer.start()
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        print("inside the except")
        my_observer.stop()
        my_observer.join()



