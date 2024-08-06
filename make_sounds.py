import pygame
from pydub import AudioSegment
from pydub.generators import Sine
import io
import numpy as np
import time
import threading

class beeper:
    # Noise making class to handle any noises needed during animations.

    def __init__(self):
        pygame.mixer.init() #initalzie the mixer so threads don't create it. 
    
    def sound_generate(self, freq, dur, waveform=None):
        sample_rate = 44100
        duration_s = dur / 1000.0
        t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)
        wave = 2 * (t * freq - np.floor(t * freq + 0.5))
        wave = (wave * 32767).astype(np.int16)

        audio_segment = AudioSegment(
        wave.tobytes(),
        frame_rate=sample_rate,
        sample_width=wave.dtype.itemsize,
        channels=1
        )
        return audio_segment
    
    def play_sound(self, song):
        melody = AudioSegment.silent(duration=0)
        for note in song:
            if note == 'a':
                print('gunk')
        
        a = self.sound_generate(440, 50, waveform='sawtooth')  # 440 Hz for 200 ms
        b = self.sound_generate(494, 200, waveform='sawtooth')  # 494 Hz for 200 ms
        c = self.sound_generate(523, 200, waveform='sawtooth')  # 523 Hz for 200 ms

        melody += a
        melody_buffer = io.BytesIO()
        melody.export(melody_buffer, format="wav")
        melody_buffer.seek(0)

        # Load the sound from the BytesIO object
        sound = pygame.mixer.Sound(melody_buffer.read())
        sound.play()