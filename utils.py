import wave
import contextlib
from pydub import AudioSegment
import wave
import os

DIR = r"C:\Users\Dell\Desktop\speech"

def stereo_to_mono(audiofile):
    sound = AudioSegment.from_wav(audiofile)
    sound = sound.set_channels(1)
    sound.export(audiofile, format="wav")

def get_duration(fname):
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate) #(in s) duration is the frames divided by fps
        return duration