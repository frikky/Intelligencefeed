#!/usr/bin/python

import gzip
from time import time
from json import loads
from sys import stdout
from wget import download 
from os import remove, path

# Check single: http://checkurl.grabber.com/checkurl/
# Make generic

class grabber(object):
    def __init__(self, name, base_url, path, filename, refreshtime, token=""):
        self.name = name
        self.base_url = base_url 
        self.path = path
        self.filename = filename 
        self.token = token if token else "" 
        self.refreshtime = refreshtime 

        self.urllist = []

    def cleanup(self):
        try:
            remove(self.filename)
        except OSError as e:
            return e 

    def open_file(self):
        return gzip.open(self.filename, "rb")

    def check_all_url(self):
        self.refresh()

        try: 
            self.urllist = [item["url"] for item in loads(self.open_file().read())]
        except IOError as e:
            self.urllist = open(self.filename).read().split("\n")

        return self.urllist

    def verify_update(self):
        try:
            if int(int(time())-int(path.getmtime(self.filename))) < self.refreshtime:
                return False 
        except OSError:
            return True

        return True

    def refresh(self):
        verify_refresh = self.verify_update()
        if not verify_refresh:
            return False

        self.cleanup() 
        stdout.write("Refreshing \"%s\" database.\n" % self.name)

        if self.token:
            #split on "%s"
            self.path = self.path.replace("%s", self.token)

        print self.base_url, self.path

        self.filename = download("%s%s" % (self.base_url, self.path))

        return True

if __name__ == "__main__":
    phish = grabber()
    phish.check_all_url()
