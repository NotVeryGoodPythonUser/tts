from collections import Counter
import json
from diphone_converter import ConvertToDiphones

counter = Counter()
with open("cs.txt", "r", encoding="utf8") as wikipedia_file:
	for idx, line in enumerate(wikipedia_file.readlines()):
		if idx%100 == 0:
			print(idx, "                ", end = "\r")
		for diphone in ConvertToDiphones(line):
			counter[diphone] += 1
with open("diphone_analysis.json", "w", encoding="utf8") as analysis:
	analysis.write(json.dumps(dict(counter)))