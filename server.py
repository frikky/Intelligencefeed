from sys import argv
from json import load
from threading import Thread
from scripts.grabber import grabber 
from socket import socket,AF_INET,SOCK_STREAM

class sock_serv(object):
    def __init__(self):
        self.config_file = "config/config.json"
        self.bind_ip = "localhost"
        try:
            self.bind_port = int(argv[1])
        except:
            print "Usage: python server <port>\nDefaulting to port 5000"
            self.bind_port = 5000

    def get_single_json(self, name):
        intel_json = load(open(self.config_file, "r"))
        for item in intel_json:
            if item["name"] == name:
                return item

        return ""

    def run_server(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.bind_ip, self.bind_port)) 

        self.server.listen(5) 
        print "[*] Listening on %s:%d" % (self.bind_ip, self.bind_port)

        while True:
            client, addr = self.server.accept()

            print "[*] Connection from %s:%d" % (addr[0], addr[1])
            client_handler = Thread(target=self.handle_client,args=(client,))
            client_handler.start()

    def usage(self, json_obj):
        data = ["[*] Usage: %s/name/command. Implemented commands:"]
        for item in json_obj:
            data.append("[*] %s: %s" % (item["name"], ", ".join(item["items"])))

        return "\n".join(data)

    def handle_client(self, client_socket):
        request = client_socket.recv(1024)
        
        # Refresh for each request in case of updates.
        json_data = load(open(self.config_file, "r"))
        intelnames = [item["name"] for item in json_data]

        #Make dynamic 
        # Find name 
        split_req = request.split("\n")
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
            request_name = request_line.split(" ")[1][1:].split("/")[0]
            request_command = request_line.split(" ")[1][1:].split("/")[1]
        except IndexError:
            client_socket.send(self.usage(json_data))
            client_socket.close()
            return
        # Above might not work

        cnt = 0
        for item in intelnames:
            if item in request_name:
                if not request_command in json_data[cnt]["items"]:
                    client_socket.send("%s for %s is not implemented.\n%s" % \
                        (request_command, request_name, self.usage))
                    break

                # Implement usage if config is not specified?
                try:
                    token = json_data[cnt]["token"]
                except (NameError, KeyError):
                    token = ""

                intel = grabber(json_data[cnt]["name"], json_data[cnt]["base_url"], \
                        json_data[cnt]["path"], json_data[cnt]["filename"], \
                        json_data[cnt]["refreshtime"], token=token)
                
                return_intel = intel.check_all_url()
                client_socket.send("%s" % "\n".join(return_intel))
                break

            cnt += 1

        client_socket.close()
         
if __name__ == "__main__":
    socks = sock_serv() 
    socks.run_server() 
