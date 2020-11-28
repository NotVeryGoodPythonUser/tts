import json

with open("diphone_analysis.json", "r") as json_file:
    dict = json.loads(json_file.read())
print(dict)
print(len(dict))
