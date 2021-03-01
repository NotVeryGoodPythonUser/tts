"""
diphone analyser
================
Script analysing number of occurrences of different diphones from cs.txt.

Converts text from cs.txt to diphones line by line using function
convertToDiphones from diphone_converter.py. Then counts number of
occurrences of each diphone and saves all data to diphone_analysis.json
as dictionary, with diphones as keys and their occurrences as values.
"""

from collections import Counter
import json

from diphone_converter import convert_to_diphones

counter = Counter()
with open("cs.txt", "r", encoding="utf8") as text_file:
	for idx, line in enumerate(text_file.readlines()):
		if idx % 100 == 0:
			print(idx, "                ", end="\r")
		for diphone in convert_to_diphones(line):
			counter[diphone] += 1
with open("diphone_analysis.json", "w", encoding="utf8") as analysis:
	analysis.write(json.dumps(dict(counter)))
