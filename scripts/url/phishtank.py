from sys import argv
import json
import gzip

filename = argv[1]

def gunzip():
    return gzip.open("%s" % filename, "rb")

url_list = []

try:
    url_path = [item["url"] for item in json.loads(gunzip().read())]
except (ValueError, IOError):
    exit()

# This is some nice code lmao
# Apparently missing one domain - not sure which - just add else.
for item in url_path:
    if item.startswith("http://"):
        tmp_item = item[7:].split("/")[0]
        if "http://%s" % tmp_item not in url_list:
            url_list.append("%s" % tmp_item)
    elif item.startswith("https://"):
        tmp_item = item[8:].split("/")[0]
        if "https://%s" % tmp_item not in url_list:
            url_list.append("%s" % tmp_item)

with open(argv[2], "w+") as dritt:
    dritt.write("\n".join(url_list))
