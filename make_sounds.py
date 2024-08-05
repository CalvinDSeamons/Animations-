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

    def hhhplay(self, song):
        melody_buffer = io.BytesIO()
        song.export(melody_buffer, format="wav")
        melody_buffer.seek(0)
        pygame.mixer.music.load(melody_buffer)
        pygame.mixer.music.play()

        # Keep the script running long enough to hear the sound
        while pygame.mixer.music.get_busy():
          pygame.time.Clock().tick(10)
        pygame.mixer.quit()






# Function to generate a beep sound
def generate_beep(frequency, duration_ms, volume=-20.0):
    beep = Sine(frequency).to_audio_segment(duration=duration_ms).apply_gain(volume)
    return beep


def generate_synth_sound(frequency, duration_ms, waveform='sawtooth'):
    sample_rate = 44100
    duration_s = duration_ms / 1000.0
    t = np.linspace(0, duration_s, int(sample_rate * duration_s), endpoint=False)

    if waveform == 'sawtooth':
        wave = 2 * (t * frequency - np.floor(t * frequency + 0.5))
    elif waveform == 'square':
        wave = np.sign(np.sin(2 * np.pi * frequency * t))
    elif waveform == 'triangle':
        wave = 2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1
    else:
        wave = np.sin(2 * np.pi * frequency * t)  # Default to sine wave

    wave = (wave * 32767).astype(np.int16)
    audio_segment = AudioSegment(
        wave.tobytes(),
        frame_rate=sample_rate,
        sample_width=wave.dtype.itemsize,
        channels=1
    )
    return audio_segment

def play_tone():
    # Generate individual notes
    a = generate_beep(440, 500)  # 440 Hz for 500 ms
    b = generate_beep(494, 500)  # 494 Hz for 500 ms
    c = generate_beep(523, 500)  # 523 Hz for 500 ms

    a = generate_synth_sound(440, 200, waveform='sawtooth')  # 440 Hz for 200 ms
    b = generate_synth_sound(494, 200, waveform='sawtooth')  # 494 Hz for 200 ms
    c = generate_synth_sound(523, 200, waveform='sawtooth') 

    # Combine notes to create a melody
    #melody = note_a + note_b + note_c + note_a + note_b + note_c + \
    #         note_c + note_c + note_c + note_c + note_b + note_b + \
    #         note_b + note_b + note_a + note_b + note_c

    #melody = c+b+a+c+b+a+a+a+a+a+b+b+b+b+c+b+a+b+c+a+a+c+b+c+a
    melody = c
    # Export the melody to a BytesIO object
    melody_buffer = io.BytesIO()
    melody.export(melody_buffer, format="wav")
    melody_buffer.seek(0)

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the sound from the BytesIO object
    pygame.mixer.music.load(melody_buffer)

    # Play the sound
    
    pygame.mixer.music.play()

    # Keep the script running long enough to hear the sound
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Stop the music if the stop event is set
    #if stop_event.is_set():
    #    pygame.mixer.music.stop()

    # Quit Pygame mixer to free resources
    pygame.mixer.quit()
