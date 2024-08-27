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
    
    def sound_generate(self, freq, dur, waveform):
        sample_rate = 44100
        duration_s = dur / 1000.0
        t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)
      

        if waveform == "sine":
            wave = np.sin(2 * np.pi * freq * t)
        elif waveform == "square":
            wave = np.sign(np.sin(2 * np.pi * freq * t))
        elif waveform == "triangle":
            wave = 2 * (t * freq - np.floor(t * freq + 0.5))
        elif waveform == "sawtooth":
            wave = 2 * (t * freq - np.floor(0.5 + t * freq))
        elif waveform == "gong":
            wave = (
                np.sin(2 * np.pi * freq * t) * np.exp(-3 * t) +
                0.5 * np.sin(2 * np.pi * (freq / 2) * t) * np.exp(-4 * t) +
                0.3 * np.sin(2 * np.pi * (freq * 1.5) * t) * np.exp(-5 * t)
            )

        elif waveform == "synth_beat":
            # Long synth tech beat sound
            # Start with a rich sawtooth base
            base_wave = 0.7 * np.sin(2 * np.pi * freq * t)  # Fundamental sine wave
            layer1 = 0.5 * np.sin(2 * np.pi * (freq * 2) * t)  # Harmonic layer
            layer2 = 0.3 * np.sin(2 * np.pi * (freq * 0.5) * t)  # Sub-harmonic layer
            saw_wave = 0.6 * (2 * (t * freq - np.floor(t * freq + 0.5)))  # Sawtooth wave

            # Combine layers
            wave = base_wave + layer1 + layer2 + saw_wave

            # Apply a decay envelope
            decay = np.exp(-2 * t)
            wave *= decay

            # Slight modulation to add depth
            modulation = 0.1 * np.sin(2 * np.pi * 0.5 * t)
            wave += modulation
        
        else:
            # Default to sine wave if waveform is not specified or recognized
            wave = np.sin(2 * np.pi * freq * t)

        # Normalize to 16-bit range and convert to int16
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

        a = self.sound_generate(440, 50,  waveform='gong')  # 440 Hz for 200 ms
        b = self.sound_generate(494, 200, waveform='sawtooth')  # 494 Hz for 200 ms
        c = self.sound_generate(523, 200, waveform='sawtooth')  # 523 Hz for 200 ms
        d = self.sound_generate(freq=220, dur=1000, waveform="synth_beat")

        melody += d
        melody_buffer = io.BytesIO()
        melody.export(melody_buffer, format="wav")
        melody_buffer.seek(0)

        # Load the sound from the BytesIO object
        sound = pygame.mixer.Sound(melody_buffer)
        sound.play()
        pygame.time.delay(1000)