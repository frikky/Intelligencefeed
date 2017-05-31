#!/usr/bin/python

import gzip
from subprocess import call
from time import time
from json import loads
from sys import stdout
from wget import download 
import os

class grabber(object):
	def __init__(self, name, base_url, path, filename, refreshtime, filter="", token=""):
		self.name = name
		self.base_url = base_url 
		self.path = path
		self.filename = filename 
		self.token = token if token else "" 
		self.refreshtime = refreshtime 
		self.filter = filter

		self.urllist = []

	def cleanup(self):
		try:
			os.remove("data/%s" % self.filename)
		except OSError as e:
			return e 

	def move_file(self):
		os.rename("%s" % self.filename, "data/%s" % self.filename)

	def check_all_url(self):
		self.refresh("url")

		dir_path = os.path.dirname(os.path.realpath(__file__))

		if not self.filter:
			self.urllist = open("%s/data/%s" % (dir_path, self.filename)).read().split("\n")
		else:
			self.urllist = open("%s/data/url/%s" % (dir_path, self.filename)).read().split("\n")

		return self.urllist

	def check_all_ip(self):
		self.refresh("ip")

		dir_path = os.path.dirname(os.path.realpath(__file__))

		if not self.filter:
			self.iplist = open("%s/data/%s" % (dir_path, self.filename)).read().split("\n")
		else:
			self.iplist = open("%s/data/ip/%s" % (dir_path, self.filename)).read().split("\n")

		return self.iplist

	def verify_update(self):
		try:
			if int(int(time())-int(os.path.getmtime("data/%s" % self.filename))) < self.refreshtime:
				return False 
		except OSError:
			return True

		return True

		# Implement ip first
	def fix_file(self, path):
		if not self.filter:
			return

		dir_path = os.path.dirname(os.path.realpath(__file__))
		args = ["python", "%s/scripts/%s/%s" % (dir_path, path, self.filter), \
			"%s/data/%s" % (dir_path, self.filename),
			"%s/data/%s/%s" % (dir_path, path, self.filename)]

		#print(" ".join(args))

		call([" ".join(args)], shell=True)

		# Add ALL, IP, Hash, URL etc.

	def refresh(self, path):
		verify_refresh = self.verify_update()

		## FIX -- MIGHT BREAK SHIT
		#self.fix_file(path)

		if not verify_refresh:
		   return False

		self.cleanup() 
		stdout.write("Refreshing \"%s\" database.\n" % self.name)

		if self.token:
			self.path = self.path.replace("%s", self.token)

                print "%s%s" % (self.base_url, self.path)
                try:
                    self.filename = download("%s%s" % (self.base_url, self.path))
                except IOError:
                    print "Might be error in URL."
                    return False 

		self.move_file()
		self.fix_file(path)

		return True

if __name__ == "__main__":
        phish = grabber("zeus", "https://zeustracker.abuse.ch/", 
            "blocklist.php?download=ipblocklist", 
            "blocklist.php?download=ipblocklist", 
             43200, "zeus.py")
	#phish = grabber("bambenek", "http://osint.bambenekconsulting.com", "/feeds/c2-ipmasterlist.txt", "c2-ipmasterlist.txt", 43200, "bambenek.py")

	print("\n".join(phish.check_all_ip()))
