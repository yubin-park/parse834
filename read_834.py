from pprint import pprint
from collections import Counter
import csv

fn_in = "INPUTFILENAME.txt"
fn_out = "OUTPUTFILENAME.csv"

rawdata = ""
with open(fn_in, "r") as fp:
    rawdata = "~".join([line for line in fp.readlines()])

data = []
doc = {"prefix": ""}
header = Counter()
for line in rawdata.split("~"):
    tokens = line.split("*")
    if tokens[0] == "INS": 
        del doc["prefix"]
        if "NM1*IL" in doc:
            data.append(doc)
            for key in doc.keys():
                header[key] += 1
        doc = {"prefix": ""}
    elif tokens[0] in {"REF", "NM1", "N1", "PER", 
                    "PLA", "DMG", "LUI", "HD", "DTP"}:
        key = doc["prefix"] + "*".join(tokens[:2])
        doc[key] = "*".join(tokens[2:])
    elif tokens[0] in {"N3", "N4"}:
        key = doc["prefix"] + tokens[0]
        doc[key] = "*".join(tokens[1:])
    elif tokens[0] in {"LX", "LS"}:
        if "LS*2700*" in doc["prefix"]:
            doc["prefix"] = "LS*2700*" + "*".join(tokens[:2]) + "*"
        else:
            doc["prefix"] = "*".join(tokens[:2]) + "*"

header = [pair[0] for pair in header.most_common()]
with open(fn_out, "w") as fp:
    writer = csv.writer(fp)
    writer.writerow(header)
    for doc in data:
        row = [doc.get(key, "") for key in header]
        writer.writerow(row)


