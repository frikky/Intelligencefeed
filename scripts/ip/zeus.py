from sys import argv

with open(argv[1], "r") as tmp:
    stuff = tmp.read()

iplist = [] 

for line in stuff.split("\n"):
    if line.startswith("#"):
        continue

    if not line or len(line) < 6:
        continue 

    if not line[0].isdigit():
        continue


    iplist.append(line)

with open(argv[2], "w+") as tmp:
    tmp.write("\n".join(iplist))
