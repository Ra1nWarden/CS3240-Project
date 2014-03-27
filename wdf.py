import sys
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print create_time, event.event_type, event.src_path
        """if event.is_directory:
            print create_time, event.event_type, event.src_path
        else:
            print create_time, event.event_type, event.src_path
"""
    def on_deleted(self, event):
        delete_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print delete_time, event.event_type, event.src_path
        """if event.is_directory:
            print delete_time, event.event_type, event.src_path
        else:
            print delete_time, event.event_type, event.src_path
"""
    def on_modified(self, event):
        modify_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print modify_time, event.event_type, event.src_path
        """if not event.is_directory:
            print modify_time, event.event_type, event.src_path
"""
    def on_moved(self, event):
        move_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print move_time, "moved from", event.src_path, "to", event.dest_path


def upload():
    print "wait for uploading"

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
