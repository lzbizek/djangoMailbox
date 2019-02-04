#!/usr/bin/python

import threading
import time
import poczta

class myThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while(True):
			poczta.sprawdzPoczte()
			print "mail updated"
			time.sleep(30)