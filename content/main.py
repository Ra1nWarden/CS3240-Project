import pynotify
import gtk
import appindicator
import thread
import threading
import time
from client import Watcher
from client import sync

class ErrorMessage:
    def delete_event(self, widget, event, data=None):
        widget.hide()
        return True
    def done_event(self, widget, data=None):
        self.window.hide()
        return True
    def show(self):
        self.window.show()
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(200, 200)
        self.window.set_title("Error")
        self.window.connect("delete_event", self.delete_event)
        
        rows = gtk.VBox(True, 5)
        self.window.add(rows)
        rows.show()

        message = gtk.Label("Invalid username/password\n combination")
        rows.pack_start(message, True, True, 0)
        message.show()

        doneButton = gtk.Button("Done")
        doneButton.connect("clicked", self.done_event)
        rows.pack_start(doneButton, True, True, 0)
        doneButton.show()
        

class LoginWindow:
    def delete_event(self, widget, event, data=None):
        widget.hide()
        return True

    def submit_info(self, widget, data=None):
        self.username = self.nameentry.get_text()
        self.password = self.passwordentry.get_text()
        self.window.hide()
        return False

    def submitbutton_connect(self, callback):
        self.submitbutton.connect("clicked", callback)

    def show(self):
        self.nameentry.show()
        self.passwordentry.show()
        self.window.show()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(400,200)
        self.window.set_title("Log in")
        self.window.connect("delete_event", self.delete_event)

        rows = gtk.VBox(True, 5)
        self.window.add(rows)
        rows.show()

        namelabel = gtk.Label("Username:")
        rows.pack_start(namelabel, True, True, 5)
        namelabel.show()
        
        self.nameentry = gtk.Entry()
        self.nameentry.set_max_length(50)
        self.nameentry.set_visibility(True)
        self.nameentry.set_editable(True)
        rows.pack_start(self.nameentry, True, True, 0)
        self.nameentry.show()

        passwordlabel = gtk.Label("Password:")
        rows.pack_start(passwordlabel, True, True, 0)
        passwordlabel.show()

        self.passwordentry = gtk.Entry()
        self.passwordentry.set_max_length(50)
        self.passwordentry.set_visibility(False)
        self.passwordentry.set_editable(True)
        rows.pack_start(self.passwordentry, True, True, 0)
        self.passwordentry.show()

        separator = gtk.VSeparator()
        rows.pack_start(separator, True, True, 0)
        separator.show()
        
        self.submitbutton = gtk.Button("Submit")
        self.submitbutton.connect("clicked", self.submit_info)
        rows.pack_start(self.submitbutton, True, True, 0)
        self.submitbutton.show()

        self.username = None
        self.password = None

class Application:
    def check_match(self, user, key):
        # to be filled up with log in code
        return True
    def login_pop(self, widget, data=None):
        self.popwindow.show()
    def log_out(self, widget, data=None):
        self.logini.show()
        self.switchi.hide()
        self.logouti.hide()
        self.login = False
        self.username = None
    def get_sync_path(self):
        return self.watcher.path
    def check_info(self, widget, data=None):
        entered_username = self.popwindow.username
        entered_password = self.popwindow.password
        if self.check_match(entered_username, entered_password):
            self.logini.hide()
            self.logouti.show()
            self.switchi.show()
            self.login = True
            self.username = entered_username
        else:
            self.errorMsg.show()
        return True
    def quit_app(self, widget, data=None):
        self.running = False
        gtk.main_quit()
    def switch_toggle(self, widget, data=None):
        self.syncswitch = widget.get_active()
        if self.syncswitch:
            self.watcher.start_watching()
        else:
            self.watcher.pause_watching()
    def __init__(self):
        self.indicator = appindicator.Indicator('oneDir', '/home/zihao/Dropbox/Documents/UVa/Spring 2014/CS 3240/CS3240-Project/content/icons/icon.ico', appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.mainMenu = gtk.Menu()
        self.errorMsg = ErrorMessage()
        self.quiti = gtk.MenuItem('Quit')
        self.quiti.connect('activate', self.quit_app)
        self.switchi = gtk.CheckMenuItem('Sync')
        self.switchi.connect('activate', self.switch_toggle)
        self.logini = gtk.MenuItem('Log in')
        self.logini.connect('activate', self.login_pop)
        self.logouti = gtk.MenuItem('Log out')
        self.logouti.connect('activate', self.log_out)
        self.mainMenu.append(self.switchi)
        self.mainMenu.append(self.logini)
        self.mainMenu.append(self.logouti)
        self.mainMenu.append(self.quiti)
        self.popwindow = LoginWindow()
        self.popwindow.submitbutton_connect(self.check_info)
        self.indicator.set_menu(self.mainMenu)
        self.quiti.show()
        self.logini.show()
        self.login = False
        self.syncswitch = False
        self.username = None
        self.running = True
        self.watcher = Watcher("test_dir/")

def syncing(app):
    while True:
        for i in range(0, 60):
            if not app.running:
                exit(0)
            time.sleep(1)
        if app.syncswitch:
            sync(app.get_sync_path())

if __name__ == "__main__":
    application = Application()
    gtk.gdk.threads_init()
    gtk_thread = threading.Thread(target=gtk.main, args=())
    gtk_thread.start()
    sync_thread = threading.Thread(target=syncing, args=(application,))
    sync_thread.start()
