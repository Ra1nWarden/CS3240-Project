import pynotify
import gtk
import appindicator

app = appindicator.Indicator('oneDir', '/home/zihao/Dropbox/Documents/UVa/Spring 2014/CS 3240/CS3240-Project/content/icons/icon.ico', appindicator.CATEGORY_APPLICATION_STATUS)
app.set_status(appindicator.STATUS_ACTIVE)
mainMenu = gtk.Menu()
quiti = gtk.MenuItem('Quit')
mainMenu.append(quiti)
def quitfun(item):
    gtk.main_quit()
quiti.connect('activate', quitfun)
app.set_menu(mainMenu)
quiti.show()

gtk.main()
