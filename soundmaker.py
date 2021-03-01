"""
Soundmaker
==========
Module that allows user to create wav file from sequence of diphones
and play it. Uses module *simpleaudio*

functions
---------
* play_diphones - plays diphones given as list or tuple
* concatenate_wavs - creates one wav file from multiple wav files
* choose_wavs - chooses best available wav files to represent sequence
    of diphones
* play_wav - plays given wav file
"""
import wave
import os
import simpleaudio as sa


def play_diphones(diphones):
    """
    plays diphones given as list or tuple in parameter diphones

    combines all other functions from module *soundmaker*, also saves the
    output as *sound_output.wav*

    :param list[str] diphones: diphones to play. List or tuple of
        strings long 2 characters
    :return: PlayObject from module simpleaudio, when parameter
        diphones is empty returns None
    :rtype: sa.PlayObject or None
    """
    wav_names = choose_wavs(diphones)
    result_wav = concatenate_wavs(wav_names)
    return play_wav(result_wav)


def concatenate_wavs(file_name_list, result_path="sound_output.wav"):
    """
    concatenates given wav files

    :param list[str] file_name_list: list or tuple containing paths to
        files that should be concatenated
    :param str result_path: path to where the result wav file should be
        stored, default is 'sound_output.wav'
    :return: path to the result wav file
    :rtype: str
    """
    if len(file_name_list) == 0:
        return
    params = None
    all_frames = []
    nframes = 0
    for wav_file_name in file_name_list:
        with wave.open(wav_file_name, "rb") as wav_file:
            if not params:
                params = wav_file.getparams()
            all_frames.append(wav_file.readframes(wav_file.getnframes()))
            nframes += wav_file.getnframes()
    with wave.open(result_path, "wb") as output_file:
        output_file.setparams(params)
        for frames in all_frames:
            output_file.writeframes(frames)
    return result_path


def choose_wavs(diphones):
    """
    chooses best available wav files to represent sequence of diphones

    :param list[str] diphones: list or tuple of diphones to choose wav
        files for
    :return: list of paths to choosed wav files
    :rtype: list[str]
    """
    def escape(unknown_diphone):
        """
        finds diphones to replace diphone that has no corresponding wav file

        :param str unknown_diphone: diphone that should be replaced
        :return: list of two substitute diphones
        :rtype: list[str]
        """
        return [unknown_diphone[0]+"-", "-"+unknown_diphone[1]]

    wav_names = []
    available = os.listdir("diphone_resources/")
    for filename in available:
        if not (filename.endswith(".wav") and len(filename) == 6):
            available.remove(filename)
    for diphone in diphones:
        diphone_wav = diphone + ".wav"
        if diphone_wav in available:
            wav_names.append(os.path.join("diphone_resources", diphone_wav))
        else:
            for escape_diphone in escape(diphone):
                diphone_wav = escape_diphone+".wav"
                if diphone_wav in available:
                    wav_names.append(os.path.join("diphone_resources", diphone_wav))
    return wav_names


def play_wav(sound_wav):
    """
    plays given wav file

    :param str sound_wav: path to the wav file that should be played
    :return: PlayObject from module simpleaudio, when parameter
        diphones is empty returns None
    :rtype: sa.PlayObject or None
    """
    if not sound_wav:
        return
    if os.path.exists(sound_wav):
        wave_obj = sa.WaveObject.from_wave_file(sound_wav)
        return wave_obj.play()
