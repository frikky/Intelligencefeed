from sys import argv

ip_list = []

[ip_list.append(line) for line in open(argv[1], "r").read().split("\n") if not line.startswith("#")]

with open(argv[1], "w+") as dritt:
    dritt.write("\n".join(ip_list))
