"""
word searcher
=============
this script finds set of words from syn2015_word_utf8.tsv that includes
500 most common diphones. The words are saved to words_to_read.txt.
"""

import json
from collections import Counter

from diphone_converter import convert_to_diphones

with open("syn2015_word_utf8.tsv", "r", encoding="utf8") as words_file:
    possible_words = []
    for line in words_file:
        words = line.split()
        if words[0].isdigit():
            word = words[1]
        else:
            word = words[0]
        if word[-1] != "." and word[0].islower():
            possible_words.append(word)


with open("diphone_analysis.json", "r", encoding="utf8") as json_file:
    diphones = json.loads(json_file.read())

diphones = Counter(diphones)
print(diphones)
diphones = diphones.most_common(500)
diphones = [diphone[0] for diphone in diphones]

not_found = diphones
found = []
final_word_results = {}
while len(not_found) > 0:
    diphone = not_found[0]
    print(f"{len(not_found)} diphones remaining")
    for word in possible_words:
        word_diphones = convert_to_diphones(word)
        if diphone in word_diphones:
            added_by_word = []
            for diphone_from_word in word_diphones:
                if diphone_from_word in not_found:
                    not_found.remove(diphone_from_word)
                if diphone_from_word not in found:
                    found.append(diphone_from_word)
                    added_by_word.append(diphone_from_word)
            final_word_results[word] = added_by_word
            break
    if len(not_found) > 0 and not_found[0] == diphone:
        print(f"didn't find word with diphone {diphone}")
        not_found.pop(0)
del found, not_found

result_string = ""
for word in final_word_results:
    result_string += f"{word}: {final_word_results[word]}\n"

with open("words_to_read.txt", "w", encoding="utf8") as result_file:
    result_file.write(result_string)
