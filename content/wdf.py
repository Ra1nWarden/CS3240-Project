import sys
import time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from file_upload import sync_file
import requests

address = "http://127.0.0.1:5000"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if event.is_directory:
            print create_time, event.event_type, event.src_path
        else:
            uploadFile = {'file': open(event.src_path, 'rw')}
            upload(uploadFile)

    def on_deleted(self, event):
        delete_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if event.is_directory:
            print delete_time, event.event_type, event.src_path
        else:
            filename = event.src_path.rsplit('/')[-1]
            filerm = {'file': filename}
            removeFile(filerm)

    def on_modified(self, event):
        modify_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if event.is_directory:
            print modify_time, event.event_type, event.src_path
        else:
            uploadFile = {'file': open(event.src_path, 'rw')}
            upload(uploadFile)

    def on_moved(self, event):
        move_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print move_time, "moved from", event.src_path, "to", event.dest_path


def upload(ufile):
    print "wait for uploading"
    r = requests.post(address, files=ufile)
    
def removeFile(fname):
    r = requests.delete(address, params=fname)

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
