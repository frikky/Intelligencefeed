with open(argv[1], "r") as tmp:
    stuff = tmp.read()

iplist = [] 

for line in stuff.split("\n"):
    if line.startswith("#"):
        continue

    if not line:
        continue 

    iplist.append(line)

with open(argv[2], "w+") as tmp:
    tmp.write("\n".join(iplist))
