#!/usr/bin/python

from sys import argv
from os import stat, mkdir
from json import load
from threading import Thread
from grabber import grabber 
from socket import socket,AF_INET,SOCK_STREAM

class sock_serv(object):
	def __init__(self):
		self.config_file = "config/config.json"
		self.bind_ip = "127.0.0.1"
		try:
			self.bind_port = int(argv[1])
		except:
			print("Usage: python server <port>\nDefaulting to port 5000")
			self.bind_port = 5000

		self.verify_data_folder()

	def get_single_json(self, name):
		intel_json = load(open(self.config_file, "r"))
		for item in intel_json:
			if item["name"] == name:
				return item

			return ""

	def verify_data_folder(self):
		try:
			stat("data/")
		except:
			mkdir("data/")
			mkdir("data/ip")
			mkdir("data/url")
			mkdir("data/hash")
			print("Created data folder for first runtime.")

	def run_server(self):
		self.server = socket(AF_INET, SOCK_STREAM)
		self.server.bind((self.bind_ip, self.bind_port)) 

		self.server.listen(5) 
		print("[*] Listening on %s:%d" % (self.bind_ip, self.bind_port))

		while True:
			client, addr = self.server.accept()

			print("[*] Connection from %s:%d" % (addr[0], addr[1]))
			client_handler = Thread(target=self.handle_client,args=(client,))
			client_handler.start()

	def usage(self, json_obj):
		data = ["[*] Usage: %s/name/command. Implemented commands:"]

		# Add categories together
		for item in json_obj:
			data.append("[*] %s: %s" % (item["category"], ", ".join(item["items"])))

		return "\n".join(data)

	def handle_client(self, client_socket):
		request = client_socket.recv(1024)

		# Refresh for each request in case of updates.
		json_data = load(open(self.config_file, "r"))
		intelnames = [item["name"] for item in json_data]
		intelcategories = [item["category"] for item in json_data]

		split_req = str(request).split("\n")

		request_line = ""
		for i in range(len(split_req)):
			if "GET /" in split_req[i] and not "GET /favico" in split_req[i]:
				request_line = split_req[i] 
				break

		if not request_line:
			client_socket.send(self.usage(json_data))
			client_socket.close()
			return

		# It works \o/
		try:
			request_category = request_line.split(" ")[1][1:].split("/")[0]
			request_command = request_line.split(" ")[1][1:].split("/")[1]
		except IndexError:
			print("Sending usage to user.")
			client_socket.send(self.usage(json_data))
			client_socket.close()
			return
		# Above might not work

		total_values = []

		cnt = 0
		for item in intelcategories:
			if not item in request_category:
				cnt += 1
				continue

			if not request_command in json_data[cnt]["items"]:
				print(request_command, json_data[cnt])
				client_socket.send("%s for %s is not implemented.\n\n%s" \
					% (request_command, request_category, self.usage(json_data)))
				cnt += 1
				continue

			# Used if a token is necessary to grab the data
			try:
				token = json_data[cnt]["token"]
			except (NameError, KeyError):
				token = ""

			# Used if a filter is specified to gain the right information
			try:
				filter = json_data[cnt]["filters"]
			except (NameError, KeyError):
				filter = ""

			# Add category indexing for the returned info
			intel = grabber(json_data[cnt]["name"], json_data[cnt]["base_url"], \
					json_data[cnt]["path"], json_data[cnt]["filename"], \
					json_data[cnt]["refreshtime"], \
					filter=filter, token=token)

			cnt += 1

			if request_command == "url":
				total_values.extend(intel.check_all_url())
			elif request_command == "ip":
				total_values.extend(intel.check_all_ip())

		# Verify multiple of the same here
		if not total_values:
			print("Sending usage at end (135)")
			client_socket.send("%s for %s is not implemented.\n\n%s" % \
				(request_command, request_category, self.usage(json_data)))
		else:
			client_socket.send("%s" % "\n".join(total_values))
			total_values = []

		client_socket.close()

if __name__ == "__main__":
	socks = sock_serv() 
	socks.run_server() 
