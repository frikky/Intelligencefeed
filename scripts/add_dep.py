import json
import pprint
from grabber import grabber

class config_setup(object):
    def __init__(self, name="", token="", base_url="", filepath="", \
                refreshtime="", file="../config/config.json"):
        self.filelocation = file
        self.name = name 
        self.token = token 
        self.base_url = base_url 
        self.filepath = filepath 
        self.refreshtime = refreshtime 

    def get_file(self):
        return json.load(open(self.filelocation, "r"))

    def write_file(self):
        structure = {
            "name": self.name, 
            "base_url": self.base_url,
            "path": self.filepath,
            "refreshtime": 43200,
        }
        if self.token:
            structure["token"] = self.token

        json_data = self.get_file()
        json_data.append(structure)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(json_data)

        with open(self.filelocation, "w") as lol:
            json.dump(json_data, lol, indent=8)

    def add_dep(self):
        print "--- For those too lazy to write raw json --- \nRemember to check the lay of the lands\n"
        while(1):
            break
            if not self.name:
                self.name = raw_input("[*] Name: ")
                if not self.name:
                    print "[!!!] No name specified. "
                    continue

            if not self.token:
                if self.filepath and not "%s" in self.filepath:
                    self.token = 0
                    continue

                self.token = raw_input("[*] Token (blank if you dont know): ")
                if "%s" in self.filepath and not self.token:
                    print "Since filepath is specified with %s a token is needed!!!!"

                if self.token:
                    print("[!!!] Since token is specified, filepath (not base_url) needs to contain %s for the location to use the token.")

                if not self.token: 
                    self.token = False

            if not self.base_url:
                self.base_url = raw_input("[*] Base_url: ")
                if not self.base_url:
                    print "[!!!] OMG"
                    continue

            if not self.filepath:
                self.filepath = raw_input("[*] Filepath: ")
                if not self.filepath.startswith("/"):
                    print "[!!!] Invalid path - needs to start with /"
                    self.filepath = ""
                    continue

                if self.token and not "%s" in self.filepath:
                    print "Filepath needs to contain an %s since a token is described."
                    self.filepath = ""

            if not self.refreshtime:
                try:
                    self.refreshtime = int(raw_input("[*] Reload limit: "))
                except ValueError:
                    print "Needs to be integer." 
                    continue

                if self.refreshtime < 3600:
                    print "Refresh time is less than an hour, be cautious if big files :)"

            if self.name and self.base_url and self.filepath and self.refreshtime:
                print "\n--- Collected data ---\n"
                print "Name: %s" % self.name
                print "File: %s%s" % (self.base_url, self.filepath)
                if self.token != 0:
                    print "Token (will be replaced at runtime): %s" % self.token
                print "Refresh: %d" % self.refreshtime
                break

        self.write_file()

if __name__ == "__main__":
    config = config_setup(name="test", base_url="google.com", filepath="/halvor", refreshtime=3600)
    config.add_dep()
