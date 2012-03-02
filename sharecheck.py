import os, sys, getpass

from twisted.internet import glib2reactor
glib2reactor.install()
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

from twisted.internet import defer, reactor

from ubuntuone.platform.tools import SyncDaemonTool

class ShareAccept():
	def __init__(self):
		print "init"
		self.sd = SyncDaemonTool()

		self.detect_shares()

	@defer.inlineCallbacks
	def detect_shares(self):
		print "Detecting shares..."
		self.sd.refresh_shares()
		l = yield self.sd.get_shares()
		for s in l:
			volume_id = str(s["volume_id"])
			if s["accepted"] == "":
				print "...FOUND NEW SHARE: " + str(s["name"]) + " (" + str(s["volume_id"]) + ")"
				print "...accepting share: " + volume_id
				res = yield self.sd.accept_share(volume_id)
			if s["subscribed"] == "":
				print "...subscribing to share: " + volume_id
				sub = yield self.sd.subscribe_share(volume_id)
				print "...done!"
		print "Completed."
		reactor.stop()		

if __name__ == '__main__':
	s = ShareAccept()
	DBusGMainLoop(set_as_default=True)
	reactor.run()
