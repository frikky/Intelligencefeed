import json
import socket
import qradar

class qradar_replace(object):
    def __init__(self, server, port):
	self.siem = ""
        self.threatserver = server
        self.threatport = port

    # Verifies if the name contains space
    def check_refname(self, name):
        if " " in name:
            return "%2520".join(name.split(" "))
        else:
            return name

    # Grabs data from the intelframework running
    def get_data(self, category, variable):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.threatserver, self.threatport))
        client.send("GET /%s/%s HTTP/1.0" % (category, variable))

        response = client.recv(1000000)
        
        return response

    # Makes the data usable in the right format
    def fix_text(self, data):
        string_compile = "["
        for item in data.split("\n"):
            if item:
                string_compile += "\'%s\'," % item

        string_compile = string_compile[:-1]
        string_compile += "]"
        return string_compile

    # Bulk loads data to the specified name
    def add_to_list(self, name, path, data):
        data = self.fix_text(data)

        try:
            response = self.siem.post("%s/bulk_load/%s" % (path, name), data=data)
        except qradar.qradarbase.QRadarError:
            return False 
        return True

    def create_ref_set(self, path, name, type, variable):
        if not variable.upper() == "IP":
            variable = "ALN"

        url = "%s?element_type=%s&name=%s" % (path, variable.upper(), name)
        if type == "dynamic":
            url += "&time_to_live=12%20hours"

        # Trycatch because of error in pyQRadar
        try:
            self.siem.post(url)
        except KeyError: 
            pass

        return True

    def verify_ref_set(self, path, name):
        try:
            self.siem.get("%s/%s" % (path, name), headers=self.siem.header)
            return True
        except qradar.qradarbase.QRadarError:
            return False

    # Clears a reference set
    def clear_list(self, name, path):
        url = "%s/%s?purge_only=true" % (path, name)
        try:
            ret = self.siem.delete(url)
        except qradar.qradarbase.QRadarError:
            return False

        return ret

    # Verify existence of reference set and create if it doesn't exist.	
    # Appends or refreshes a reference set with new data.
    def iter_refsets(self, ref_item):
        for ref_list in ref_item["lists"]:
            ref_list["name"] = self.check_refname(ref_list["name"])

            path = "reference_data/sets"
                
            if ref_list["type"].lower() == "dynamic" or ref_list["type"].lower() == "static":
                data = self.get_data(ref_list["category"], ref_list["variable"])

                # Verify if exists here, else create.
                ref_status = self.verify_ref_set(path, ref_list["name"])
                if not ref_status:
                    ret = self.create_ref_set(path, ref_list["name"], \
                        ref_list["type"], ref_list["variable"])
                    if not ret:
                        continue
                
                if ref_list["type"].lower() == "dynamic":
                    clear = self.clear_list(ref_list["name"], path)

                print "Adding data to \"%s\"" % " ".join(ref_list["name"].split("%2520"))
                ret = self.add_to_list(ref_list["name"], path, data)
                if not ret:
                    print "SHOULD REITER - Wasn't able to add data to %s" % ref_list["name"]
            else:
                print "Invalid type for list %s" % ref_list["name"] 
                continue

    # Iterates the qradar systems
    def iter_systems(self):
        for item in json.load(open("systems.json", "r")):
            self.siem = qradar.QRadar(item["host"], item["SEC"])
            done = self.iter_refsets(item)

            if not done:
                    continue

    
if __name__ == "__main__":
    replace = qradar_replace("", )
    replace.iter_systems()
