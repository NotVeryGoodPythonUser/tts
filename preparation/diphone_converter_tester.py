"""
diphone_converter tester
========================
this script enables user to test module diphone_converter.py
"""
from diphone_converter import convert_to_diphones
print("if you want to quit, type quit")
while True:
    test_phrase = input("test phrase: ")
    if test_phrase == "quit":
        break
    print(convert_to_diphones(test_phrase))
