import wave
import contextlib
from pydub import AudioSegment
import os
import PyWave as pw
import warnings

warnings.filterwarnings('ignore')

DIR = r"C:\Users\Dell\Desktop\speech"

class AudioFile:
    def __init__(self, path_to_file):
        self.path_to_file = path_to_file

    def stereo_to_mono(self):
        wf = pw.open(self.path_to_file)
        if wf.channels != 1:
            sound = AudioSegment.from_wav(self.path_to_file)
            sound = sound.set_channels(1)
            sound.export(self.path_to_file, format="wav")    

    def get_duration(self):
        with contextlib.closing(wave.open(self.path_to_file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate) #(in s) duration is the frames divided by fps
            return duration

    def trim_audio(self, t1, t2):
        t1 = t1 * 1000 #Works in milliseconds
        t2 = t2 * 1000
        newAudio = AudioSegment.from_wav(self.path_to_file)
        newAudio = newAudio[t1:t2]
        newAudio.export('trimmed.wav', format="wav")

if __name__ == "__main__":
    audio = AudioFile("../testing/trimmed.wav")
    duration = audio.get_duration()
    print(duration) # confirms the duration 
    