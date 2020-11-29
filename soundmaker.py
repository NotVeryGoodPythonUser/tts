import wave
import os
import simpleaudio as sa


def concatenatewavs(file_name_list, result_path="sound_output.wav"):
    params = None
    all_frames = []
    nframes = 0
    for wav_file_name in file_name_list:
        with wave.open(wav_file_name, "rb") as wav_file:
            if not params:
                params = wav_file.get_params()
            all_frames.append(wav_file.readframes(wav_file.getnframes()))
            nframes += wav_file.getnframes()
    with wave.open(result_path, "wb") as output_file:
        output_file.setparams(params)
        for frames in all_frames:
            output_file.writeframes(frames)
        output_file.setnframes(nframes)
    return result_path


def choosewavs(diphones):
    wav_names = []
    available = os.listdir("diphone_resources/")
    for filename in available:
        if not (filename.endswith(".wav") and len(filename) == 6):
            available.remove(filename)
    for diphone in diphones:
        diphone_wav = diphone + ".wav"
        if diphone_wav in available:
            wav_names.append(os.path.join("diphone_resources", diphone_wav))
    return wav_names


def playwav(sound_wav):
    wave_obj = sa.WaveObject.from_wave_file(sound_wav)
    wave_obj.play().wait_done()


def playdiphones(diphones):
    wav_names = choosewavs(diphones)
    result_wav = concatenatewavs(wav_names)
    playwav(result_wav)
