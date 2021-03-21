"""
diphone_converter tester
========================
this script enables user to test module diphone_converter.py
"""
from diphone_converter import convert_to_diphones
print("Pro ukončení skriptu napiš quit.")
while True:
    test_phrase = input("testovací text: ")
    if test_phrase == "quit":
        break
    print(convert_to_diphones(test_phrase))
