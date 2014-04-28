import sys
import time
import os
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests

address = "http://127.0.0.1:5000"

class MyHandler(FileSystemEventHandler):
    def on_created(self, event):
        create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print create_time, event.event_type, event.src_path
        if event.is_directory:
            print create_time, event.event_type, event.src_path
        else:
            try:
                uploadFile = {'file': open(event.src_path, 'rw')}
                upload(uploadFile)
            except:
                pass

    def on_deleted(self, event):
        delete_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print delete_time, event.event_type, event.src_path
        if event.is_directory:
            print delete_time, event.event_type, event.src_path
        else:
            filename = event.src_path.rsplit('/')[-1]
            try:
                filerm = {'file': filename}
                removeFile(filerm)
            except:
                pass

    def on_modified(self, event):
        modify_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print modify_time, event.event_type, event.src_path
        if event.is_directory:
            print modify_time, event.event_type, event.src_path
        else:
            try:
                uploadFile = {'file': open(event.src_path, 'rw')}
                upload(uploadFile)
            except:
                pass

    def on_moved(self, event):
        move_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print move_time, "moved from", event.src_path, "to", event.dest_path


def upload(ufile, username):
    args = {}
    args['username'] = username
    r = requests.post(address + "/main", files=ufile, params=args)

def download(ufile, dir, username):
    ufile['username'] = username
    r = requests.get(address + "/main", params=ufile)
    filename = r.headers['content-disposition'].rsplit('filename=')[-1]
    filename = "./" + dir + filename
    with open(filename, 'wb') as fw:
        for chunk in r.iter_content(128):
            fw.write(chunk)
    
def removeFile(fname, username):
    fname['username'] = username
    r = requests.delete(address + "/main", params=fname)

def authenticate(username, password):
    arguments = {}
    arguments['username'] = username
    arguments['password'] = password
    r = requests.post(address + "/login", params=arguments)
    return r.json()['success']

def register_user(username, password):
    arguments = {}
    arguments['username'] = username
    arguments['password'] = password
    r = requests.post(address + "/register", params=arguments)
    return r.json()['success']

def log_out():
    r = requests.post(address + "/logout")
    return r.status_code == 200

def sync(dir, username):
    fnames = os.listdir("./test_dir/")
    file_info = {}
    for each in fnames:
        file_info[each] = os.path.getmtime(os.path.join("./test_dir/", each)) 
    file_info['username'] = username
    r = requests.get(address + "/query", params=file_info)
    tobeupload = r.json()["upload"]
    tobedownload = r.json()["download"]
    for each in tobeupload:
        file_dir = "./" + dir + each
        uploadFile = {'file': open(file_dir, 'rw')}
        upload(uploadFile, username)
    for each in tobedownload:
        filedownload = {'file': each}
        download(filedownload, dir, username)

class Watcher:
    def __init__(self, dir):
        self.path = dir
        self.event_handler = MyHandler()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=True)
    
    def start_watching(self, username):
        sync(self.path, username)
        self.observer.start()

    def pause_watching(self):
        self.observer.stop()
        self.observer = Observer()
        self.observer.schedule(self.event_handler, self.path, recursive=True)

if __name__ == "__main__":
    myWatcher = Watcher("test_dir/")
    myWatcher.start_watching()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        myWatcher.pause_watching()
