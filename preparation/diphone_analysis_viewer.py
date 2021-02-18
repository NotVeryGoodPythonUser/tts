"""diphone analysis viewer

this script allows user to view analysis of diphone occurrences
in file diphone_analysis.json, created by script diphone_analyser.py.
"""
import json

with open("diphone_analysis.json", "r") as json_file:
    dict = json.loads(json_file.read())
    dict = {diphone: dict[diphone] for diphone in sorted(dict, key=dict.get, reverse=True)}
print(f"analyzed {len(dict)} diphones\n")
print("first 100:")
i=0
for diphone in dict:
    if i <100:
        i += 1
    else:
        break
    print(diphone, ":", dict[diphone])
print()
print("to get number of occurrences of particular diphone, type it.\n"
      "if you want to quit, type quit.")
while True:
    question = input("> ")
    if question == "quit":
        break
    if question in dict:
        print(dict[question])
    else:
        print("this diphone was not found")