import pygame
import random
import math
import time
import imageio
import numpy as np
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.generators import Sine
import threading 
import time

from make_sounds import beeper




def make_sounds():
    SAMPLE_RATE = 44100  # Samples per second
    DURATION = 2.0       # Duration of each note in seconds

    # Note frequencies (in Hz)
    NOTE_FREQS = {
    'C': 261.63,
    'C#': 277.18,
    'D': 293.66,
    'D#': 311.13,
    'E': 329.63,
    'F': 349.23,
    'F#': 369.99,
    'G': 392.00,
    'G#': 415.30,
    'A': 440.00,
    'A#': 466.16,
    'B': 493.88,
    }

    def generate_sine_wave(frequency, duration, sample_rate):
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Generate sine wave
        return wave

    def save_wave(filename, wave, sample_rate):
        write(filename, sample_rate, wave.astype(np.float32))

    def generate_and_save_chimes(notes, sample_rate, duration):
        for note in notes:
            if note in NOTE_FREQS:
                frequency = NOTE_FREQS[note]
                wave = generate_sine_wave(frequency, duration, sample_rate)
                filename = f"{note}.wav"
                save_wave(filename, wave, sample_rate)
                print(f"Saved {note} as {filename}")
            else:
                print(f"Note {note} not found in frequency list.")

    # Example usage
    notes_to_generate = ['A', 'B', 'F#', 'C']
    generate_and_save_chimes(notes_to_generate, SAMPLE_RATE, DURATION)


# Initialize Pygame
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bouncing Balls")
#sound = pygame.mixer.Sound("music/A.wav")

# Define constants
damping = 0.8
cooldown_time = 0.5  # Cooldown time in seconds

#make_sounds()

# Function to create a new ball
def create_ball(pos, speed, wall):
    if wall == 'left':
        angle = random.uniform(-math.pi/4, math.pi/4)  # Rightward angles
    elif wall == 'right':
        angle = random.uniform(3*math.pi/4, 5*math.pi/4)  # Leftward angles
    elif wall == 'top':
        angle = random.uniform(math.pi/4, 3*math.pi/4)  # Downward angles
    elif wall == 'bottom':
        angle = random.uniform(-3*math.pi/4, -math.pi/4)  # Upward angles
    speed_x = speed * math.cos(angle)
    speed_y = speed * math.sin(angle)
    return {
        'color': [random.randint(0, 255) for _ in range(3)],
        'pos': list(pos),
        'speed': [speed_x, speed_y],
        'radius': 20,
        'last_collision_time': time.time()
    }

# Create the initial ball
initial_speed = 3
initial_ball = {
    'color': [255, 0, 0],
    'pos': [400, 300],
    'speed': [initial_speed, 0],  # Initial horizontal speed
    'radius': 20,
    'last_collision_time': time.time()
}
balls = [initial_ball]
frames = []
# Main loop control
running = True
clock = pygame.time.Clock()

#stop_event = threading.Event()
#melody_thread = threading.Thread(target=play_tone, args=(stop_event,))
beep = beeper()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if len(balls) >= 1000:
        running = False

    # Update each ball's position
    for ball in balls:
        ball['pos'][0] += ball['speed'][0]
        ball['pos'][1] += ball['speed'][1]

        # Bounce off walls (left and right)
        if ball['pos'][0] - ball['radius'] < 0:
            ball['speed'][0] = -ball['speed'][0]
            current_time = time.time()
            if current_time - ball['last_collision_time'] > cooldown_time:
                ball['color'] = [random.randint(0, 255) for _ in range(3)]
                current_speed = math.sqrt(ball['speed'][0]**2 + ball['speed'][1]**2)
                balls.append(create_ball(ball['pos'], current_speed, 'left'))
                ball['last_collision_time'] = current_time
                threading.Thread(target=beep.play_sound, args=(['a','b'],)).start()  
                            
                
        elif ball['pos'][0] + ball['radius'] > 800:
            ball['speed'][0] = -ball['speed'][0]
            current_time = time.time()
            if current_time - ball['last_collision_time'] > cooldown_time:
                ball['color'] = [random.randint(0, 255) for _ in range(3)]
                current_speed = math.sqrt(ball['speed'][0]**2 + ball['speed'][1]**2)
                balls.append(create_ball(ball['pos'], current_speed, 'right'))
                ball['last_collision_time'] = current_time

        # Bounce off floor and ceiling
        if ball['pos'][1] - ball['radius'] < 0:
            ball['speed'][1] = -ball['speed'][1]
            current_time = time.time()
            if current_time - ball['last_collision_time'] > cooldown_time:
                ball['color'] = [random.randint(0, 255) for _ in range(3)]
                current_speed = math.sqrt(ball['speed'][0]**2 + ball['speed'][1]**2)
                balls.append(create_ball(ball['pos'], current_speed, 'top'))
                ball['last_collision_time'] = current_time
        elif ball['pos'][1] + ball['radius'] > 600:
            ball['speed'][1] = -ball['speed'][1]
            current_time = time.time()
            if current_time - ball['last_collision_time'] > cooldown_time:
                ball['color'] = [random.randint(0, 255) for _ in range(3)]
                current_speed = math.sqrt(ball['speed'][0]**2 + ball['speed'][1]**2)
                balls.append(create_ball(ball['pos'], current_speed, 'bottom'))
                ball['last_collision_time'] = current_time

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw all balls
    for ball in balls:
        pygame.draw.circle(screen, ball['color'], (int(ball['pos'][0]), int(ball['pos'][1])), ball['radius'])

    # Update display
    pygame.display.flip()
    #frame = pygame.surfarray.array3d(screen)
    #frame = np.transpose(frame, (1, 0, 2))  # Transpose to (height, width, color_channels)
    #frames.append(frame)
    clock.tick(60)

    # Save frames as a video
    imageio.mimwrite('videos/animation-1.mpeg', frames, fps=60)

pygame.quit()