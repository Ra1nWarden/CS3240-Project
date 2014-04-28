import gtk
import appindicator
import thread
import threading
import time
import webbrowser
from client import Watcher
from client import sync, register_user, authenticate, log_out, change_password

class ErrorMessage:
    def delete_event(self, widget, event, data=None):
        widget.hide()
        return True
    def done_event(self, widget, data=None):
        self.window.hide()
        return True
    def show(self):
        self.window.show()
    def __init__(self, msg):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(200, 200)
        self.window.set_title("Message")
        self.window.connect("delete_event", self.delete_event)
        
        rows = gtk.VBox(True, 5)
        self.window.add(rows)
        rows.show()

        self.message = gtk.Label(msg)
        rows.pack_start(self.message, True, True, 0)
        self.message.show()

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

    def register_new(self, widget, data=None):
        username_entered = self.nameentry.get_text()
        password_entered = self.passwordentry.get_text()
        register_success = register_user(username_entered, password_entered)
        if register_success:
            success_msg = ErrorMessage("New user successfully \n registered!")
            success_msg.show()
        else:
            fail_msg = ErrorMessage("Username in use! \n Please try again")
            fail_msg.show()

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
        
        cols = gtk.HBox(True, 5)
        cols.show()
        self.submitbutton = gtk.Button("Submit")
        self.submitbutton.connect("clicked", self.submit_info)
        self.submitbutton.show()
        cols.pack_start(self.submitbutton, True, True, 0)
        self.registerbutton = gtk.Button("Register")
        self.registerbutton.connect("clicked", self.register_new)
        self.registerbutton.show()
        cols.pack_start(self.registerbutton, True, True, 0)
        rows.pack_start(cols, True, True, 0)

        self.username = None
        self.password = None

class ChangeWindow:
    def delete_event(self, widget, event, data=None):
        widget.hide()
        return True

    def submit_info(self, widget, data=None):
        self.username = self.usernameentry.get_text()
        self.oldpassword = self.oldentry.get_text()
        self.newpassword1 = self.newentry1.get_text()
        self.newpassword2 = self.newentry2.get_text()
        self.window.hide()
        return False

    def show(self):
        self.usernameentry.show()
        self.oldentry.show()
        self.newentry1.show()
        self.newentry2.show()
        self.window.show()
    def submitbutton_connect(self, callback):
        self.submitbutton.connect("clicked", callback)
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_size_request(400,300)
        self.window.set_title("Change password")
        self.window.connect("delete_event", self.delete_event)

        rows = gtk.VBox(True, 5)
        self.window.add(rows)
        rows.show()

        usernamelabel = gtk.Label("Username:")
        rows.pack_start(usernamelabel, True, True, 5)
        usernamelabel.show()
        
        self.usernameentry = gtk.Entry()
        self.usernameentry.set_max_length(50)
        self.usernameentry.set_visibility(True)
        self.usernameentry.set_editable(True)
        rows.pack_start(self.usernameentry, True, True, 0)
        self.usernameentry.show()

        oldlabel = gtk.Label("Old password:")
        rows.pack_start(oldlabel, True, True, 5)
        oldlabel.show()
        
        self.oldentry = gtk.Entry()
        self.oldentry.set_max_length(50)
        self.oldentry.set_visibility(False)
        self.oldentry.set_editable(True)
        rows.pack_start(self.oldentry, True, True, 0)
        self.oldentry.show()

        newlabel1 = gtk.Label("New password:")
        rows.pack_start(newlabel1, True, True, 0)
        newlabel1.show()

        self.newentry1 = gtk.Entry()
        self.newentry1.set_max_length(50)
        self.newentry1.set_visibility(False)
        self.newentry1.set_editable(True)
        rows.pack_start(self.newentry1, True, True, 0)
        self.newentry1.show()

        newlabel2 = gtk.Label("Repeat password:")
        rows.pack_start(newlabel2, True, True, 0)
        newlabel2.show()

        self.newentry2 = gtk.Entry()
        self.newentry2.set_max_length(50)
        self.newentry2.set_visibility(False)
        self.newentry2.set_editable(True)
        rows.pack_start(self.newentry2, True, True, 0)
        self.newentry2.show()

        separator = gtk.VSeparator()
        rows.pack_start(separator, True, True, 0)
        separator.show()
        
        self.submitbutton = gtk.Button("Submit")
        self.submitbutton.connect("clicked", self.submit_info)
        rows.pack_start(self.submitbutton, True, True, 0)
        self.submitbutton.show()

        self.username = None
        self.oldpassword = None
        self.newpassword1 = None
        self.newpassword2 = None

class Application:
    def check_match(self, user, key):
        return authenticate(user, key)
    def login_pop(self, widget, data=None):
        self.popwindow.show()
    def log_out(self, widget, data=None):
        self.logini.show()
        self.switchi.hide()
        self.admini.hide()
        self.logouti.hide()
        self.changepasswordi.hide()
        self.login = False
        self.username = None
        self.switchi.set_active(False)
        self.syncswitch = self.switchi.get_active()
        log_out()
    def get_sync_path(self):
        return self.watcher.path
    def check_info(self, widget, data=None):
        entered_username = self.popwindow.username
        entered_password = self.popwindow.password
        if self.check_match(entered_username, entered_password):
            self.logini.hide()
            self.logouti.show()
            if entered_username == 'admin':
                self.admini.show()
            else:
                self.switchi.show()
            self.changepasswordi.show()
            self.login = True
            self.username = entered_username
            self.watcher.set_username(self.username)
        else:
            self.errorMsg.show()
        return True
    def quit_app(self, widget, data=None):
        self.running = False
        gtk.main_quit()
    def switch_toggle(self, widget, data=None):
        self.syncswitch = widget.get_active()
        if self.syncswitch:
            self.watcher.start_watching(self.username)
        else:
            self.watcher.pause_watching()
    def admin_page(self, widget, data=None):
        webbrowser.open('http://127.0.0.1:5000/admin/')
    def change_password_pop(self, widget, data=None):
        self.changepasswordwindow.show()
    def check_change(self, widget, data=None):
        entered_username = self.changepasswordwindow.username
        entered_oldpassword = self.changepasswordwindow.oldpassword
        entered_newpassword1 = self.changepasswordwindow.newpassword1
        entered_newpassword2 = self.changepasswordwindow.newpassword2
        if entered_newpassword1 != entered_newpassword2:
            match_error = ErrorMessage("Your entries did not match.")
        else:
            if self.check_match(entered_username, entered_oldpassword):
                change_password(entered_username, entered_newpassword1)
            else:
                self.errorMsg.show()
    def __init__(self):
        self.indicator = appindicator.Indicator('oneDir', '/home/zihao/Dropbox/Documents/UVa/Spring 2014/CS 3240/CS3240-Project/content/icons/icon.ico', appindicator.CATEGORY_APPLICATION_STATUS)
        self.indicator.set_status(appindicator.STATUS_ACTIVE)
        self.mainMenu = gtk.Menu()
        self.errorMsg = ErrorMessage("Invalid password/username \n combination.")
        self.quiti = gtk.MenuItem('Quit')
        self.quiti.connect('activate', self.quit_app)
        self.switchi = gtk.CheckMenuItem('Sync')
        self.switchi.connect('activate', self.switch_toggle)
        self.logini = gtk.MenuItem('Log in')
        self.logini.connect('activate', self.login_pop)
        self.logouti = gtk.MenuItem('Log out')
        self.logouti.connect('activate', self.log_out)
        self.admini = gtk.MenuItem('Admin')
        self.admini.connect('activate', self.admin_page)
        self.changepasswordi = gtk.MenuItem('Change password')
        self.changepasswordi.connect('activate', self.change_password_pop)
        self.mainMenu.append(self.switchi)
        self.mainMenu.append(self.logini)
        self.mainMenu.append(self.admini)
        self.mainMenu.append(self.changepasswordi)
        self.mainMenu.append(self.logouti)
        self.mainMenu.append(self.quiti)
        self.changepasswordwindow = ChangeWindow()
        self.changepasswordwindow.submitbutton_connect(self.check_change)
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
        for i in range(0, 20):
            if not app.running:
                exit(0)
            time.sleep(1)
        if app.syncswitch:
            sync(app.get_sync_path(), app.username)

if __name__ == "__main__":
    application = Application()
    gtk.gdk.threads_init()
    gtk_thread = threading.Thread(target=gtk.main, args=())
    gtk_thread.start()
    sync_thread = threading.Thread(target=syncing, args=(application,))
    sync_thread.start()
