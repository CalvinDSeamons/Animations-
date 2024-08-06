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
    clock.tick(60)

    # Save frames as a video
    imageio.mimwrite('videos/animation-1.mpeg', frames, fps=60)

pygame.quit()