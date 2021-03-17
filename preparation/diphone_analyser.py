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
file_to_analyse = "cs.txt"      # link to download cs.txt: https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2735/cs.txt.gz?sequence=54&isAllowed=y

counter = Counter()
with open(file_to_analyse, "r", encoding="utf8") as text_file:
    idx = 0
    for line in text_file.readlines():
        if idx % 5000 == 0:
            print(f"přečteno {idx} řádků")
        for diphone in convert_to_diphones(line):
            counter[diphone] += 1
        idx += 1
    counter = counter.most_common()
with open("diphone_analysis.json", "w", encoding="utf8") as analysis:
    analysis.write(json.dumps(dict(counter)))
