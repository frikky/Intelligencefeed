import json
import socket
import qradar
import requests

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
	def get_ip(self, category):
		client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		client.connect((self.threatserver, self.threatport))
		client.send("GET /%s/ip HTTP/1.0" % category)

		response = client.recv(65536)
		
		# Requests version for other sites
		# return requests.get("http://%s:%s/%s/ip" % (threatserver, threatport, category))

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

		response = self.siem.post("%s/bulk_load/%s" % (path, name), headers=self.siem.header, data=data)
		print response.text
		print response.status_code

	# Clears a reference set
	def clear_list(self, name, path):
		url = "%s/%s?purge_only=true" % (path, name)
		try:
			ret = self.siem.delete(url, headers=self.siem.header)
		except qradar.qradarbase.QRadarError:
			print "List is empty."
			return False

		return ret

	# Verify existence of reference set and create if it doesn't exist.	
	# Appends or refreshes a reference set with new data.
	def iter_refsets(self, ref_item):
		for ref_list in ref_item["lists"]:
			ref_list["name"] = self.check_refname(ref_list["name"])

			path = "reference_data/sets"
			
			if ref_list["type"].lower() == "dynamic" or ref_list["type"].lower() == "static":
				print "Doing magic"
				data = self.get_ip(ref_list["category"])
				if ref_list["type"].lower() == "dynamic":
					print "Clearing."
					clear = self.clear_list(ref_list["name"], path)

				self.add_to_list(ref_list["name"], path, data)
			else:
				print "Invalid type for list %s" % ref_list["name"] 
				continue
				#return False

	# Iterates the qradar systems
	def iter_systems(self):
		for item in json.load(open("systems.json", "r")):
			self.siem = qradar.QRadar(item["host"], item["SEC"])
			done = self.iter_refsets(item)

			if not done:
				continue

	
if __name__ == "__main__":
	replace = qradar_replace("127.0.0.1", 5000)
	replace.iter_systems()
