__author__ = 'zihao'

import os
from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent

wm = WatchManager()

mask = EventsCodes.IN_DELETE | EventsCodes.IN_CREATE

class PTmp(ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Create: %s" % os.path.join(event.path, event.name)

    def process_IN_DELETE(self, event):
        print "Remove: %s" % os.path.join(event.path, event.name)

notifier = Notifier(wm, PTmp())
wdd = wm.add_watch('/tmp', mask, rec=True)

while True:
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        break

# On a different thread
        
# notifier = ThreadedNotifier(wm, PTmp())
# notifier.start()
#
# wdd = wm.add_watch('/tmp', mask, rec=True)