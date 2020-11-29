import json
from diphone_converter import converttodiphones

with open("syn2015_word_utf8.tsv", "r", encoding="utf8") as words_file:
    result_list = []
    for line in words_file:
        words = line.split()
        if words[0].isdigit():
            word = words[1]
        else:
            word = words[0]
        if word[-1] != "." and word[0].islower():
            result_list.append(word)

with open("diphone_analysis.json", "r", encoding="utf8") as json_file:
    diphones = json.loads(json_file.read())
    diphones = list(diphones)

unused = diphones[:500]
final_word_results = {}
for diphone in unused:
    print(f"{len(unused)} diphones out of 500 remaining", end="\r")
    for word in result_list:
        word_diphones = converttodiphones(word)
        if diphone in word_diphones:
            for added in word_diphones:
                if added in unused:
                    unused.remove(added)
            final_word_results[word] = word_diphones
            break

for word in final_word_results:
    redundant = False
    others = final_word_results.copy()
    others.pop(word)
    for diphone in final_word_results[word]:
        diphone_found = False
        for other_word in others:
            if diphone in others[other_word]:
                diphone_found = True
                break
        if not diphone_found:
            redundant = False
            break
    if redundant:
        print(f"word {word} is redundant.\n")
        final_word_results.pop(word)

with open("words_to_read.txt", "w", encoding="utf8") as result_file:
    result_file.write("\n".join(final_word_results))
