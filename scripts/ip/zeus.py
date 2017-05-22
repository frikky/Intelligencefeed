with open(argv[1], "r") as tmp:
	stuff = tmp.read()

iplist = [] 

for line in stuff.split("\n"):
	if "<tr bgcolor" in line:
		item = line.split(" ")[7]
		iplist.append(item.split("/")[:-1])

with open(argv[2], "w+") as tmp:
	tmp.write("\n".join(iplist))
