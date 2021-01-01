import wave
import os
import simpleaudio as sa
from threading import Thread

def playdiphones(diphones):
    wav_names = choosewavs(diphones)
    result_wav = concatenatewavs(wav_names)
    return playwav(result_wav)

def concatenatewavs(file_name_list, result_path="sound_output.wav"):
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


def choosewavs(diphones):
    def escape(diphone):
        return (diphone[0]+"-", "-"+diphone[1])
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


def playwav(sound_wav):
    if not sound_wav:
        return
    if os.path.exists(sound_wav):
        wave_obj = sa.WaveObject.from_wave_file(sound_wav)
        return(wave_obj.play())


