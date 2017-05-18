#!/usr/bin/python

import gzip
from subprocess import call
from time import time
from json import loads
from sys import stdout
from wget import download 
from os import remove, path, rename

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
            remove("data/%s" % self.filename)
        except OSError as e:
            return e 

    def move_file(self):
        rename("%s" % self.filename, "data/%s" % self.filename)

    def check_all_url(self):
        self.refresh()
        self.urllist = open("data/%s" % self.filename).read().split("\n")

        return self.urllist

    def verify_update(self):
        try:
            if int(int(time())-int(path.getmtime("data/%s" % self.filename))) < self.refreshtime:
                return False 
        except OSError:
            return True

        return True

    def fix_file(self):
        if not self.filter:
            return

        dir_path = path.dirname(path.realpath(__file__))
        args = ["python", "scripts/%s" % self.filter, "%s/data/%s" % (dir_path, self.filename)]
        call([" ".join(args)], shell=True)

    def refresh(self):
        verify_refresh = self.verify_update()

        ## FIX -- MIGHT BREAK SHIT
        self.fix_file()

        if not verify_refresh:
            return False

        self.cleanup() 
        stdout.write("Refreshing \"%s\" database.\n" % self.name)

        if self.token:
            self.path = self.path.replace("%s", self.token)

        self.filename = download("%s%s" % (self.base_url, self.path))
        self.move_file()
        self.fix_file()

        return True

if __name__ == "__main__":
    phish = grabber()
    phish.check_all_url()
