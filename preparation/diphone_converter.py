"""
diphone converter
=================
Module allows user to convert text in czech to set of diphones.
Uses information stored in file convert_data.json.

functions:
    * to_supported - Changes text to contain only supported characters.
    * graphems_to_phonems - Creates phonetic transcription of text.
    * phonems_to_diphones - Creates sequence of diphones from phonetic
      transcription.
    * convert_to_diphones - Makes sequence of diphones from text.
"""
import json
import os

package_directory = os.path.dirname(os.path.abspath(__file__))
convert_data_path = os.path.join(package_directory, "convert_data.json")
with open(convert_data_path, "r", encoding="utf8") as json_data_file:
    data = json.loads(json_data_file.read())
    ALL_SUPPORTED = data["all supported"]
    CONSONANTS = data["consonants"]
    VOICED_TO_VOICELESS = data["voiced to voiceless"]
    VOICELESS_TO_VOICED = data["voiceless to voiced"]
    REPLACING_SINGLE_CHAR = data["single char replacing"]
    REPLACING_TWO_CHAR = data["two chars replacing"]
    NUM_CONVERT_DICT = data["number dict"]


def to_supported(text):
    """Changes text to contain only supported characters.

    :param str text: Text to be changed to supported characters
    :return: text containing only supported characters
    :rtype: str
    """
    text = text.lower()
    new_text = ""
    for char in text:
        if char in ALL_SUPPORTED:
            new_text += char
        elif char in NUM_CONVERT_DICT:
            new_text += NUM_CONVERT_DICT[char]
        elif char in [",", ".", "!", "?"]:
            new_text += "_"
    return new_text


def graphems_to_phonems(text):
    """Creates phonetic transcription of text.

    :param str text: text to be phonetically transcribed
    :return: phonetic transcription of text
    :rtype: str
    """
    text = to_supported(text)

    # special rules
    idx = 0
    new_text = ""
    while idx < len(text):
        if text[idx:idx + 2] in REPLACING_TWO_CHAR:
            new_text += REPLACING_TWO_CHAR[text[idx:idx + 2]]
            idx += 2
        elif text[idx] in REPLACING_SINGLE_CHAR:
            new_text += REPLACING_SINGLE_CHAR[text[idx]]
            idx += 1
        else:
            new_text += text[idx]
            idx += 1
    text = new_text
    # spodoba znělosti
    new_text = ""
    consonant_group = ""
    for char in text:
        if char in ("X", "ř"):
            for consonant in consonant_group:
                if consonant in VOICED_TO_VOICELESS:
                    new_text += VOICED_TO_VOICELESS[consonant]
                else:
                    new_text += consonant
            new_text += char
            consonant_group = ""
        elif char in CONSONANTS:
            consonant_group += char
        else:
            if len(consonant_group) > 0:
                if consonant_group[-1] in VOICED_TO_VOICELESS:
                    for consonant in consonant_group:
                        if consonant in VOICELESS_TO_VOICED:
                            new_text += VOICELESS_TO_VOICED[consonant]
                        else:
                            new_text += consonant
                elif consonant_group[-1] in VOICELESS_TO_VOICED:
                    for consonant in consonant_group:
                        if consonant in VOICED_TO_VOICELESS:
                            new_text += VOICED_TO_VOICELESS[consonant]
                        else:
                            new_text += consonant
            consonant_group = ""
            if char != " ":
                new_text += char
    print(new_text)
    return new_text


def phonems_to_diphones(text):
    """Creates sequence of diphones from phonetic transcription.

    :param str text: phonetical transcription of text
    :return: sequence of diphones, list of 2 characters long strings
    :rtype: list[str]
    """
    text = "_" + text + "_"
    diphones = []
    for idx in range(len(text) - 1):
        diphones.append(text[idx:idx + 2])
    return diphones


def convert_to_diphones(text):
    """Makes sequence of diphones from text.

    :param str text: text to be converted to diphones
    :return: sequence of diphones, list of 2 characters long strings
    :rtype: list[str]
    """
    return phonems_to_diphones(graphems_to_phonems(text))
