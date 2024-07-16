# Main method for laucnhing the annimation software. 

import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bouncing Ball")

ball_color = (255, 0, 0)
ball_pos = [400, 300]
ball_radius = 20
ball_speed = [3, 3]

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    if ball_pos[0] - ball_radius < 0 or ball_pos[0] + ball_radius > 800:
        ball_speed[0] = -ball_speed[0]
        ball_color = [random.randint(0, 255) for _ in range(3)]

    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > 600:
        ball_speed[1] = -ball_speed[1]
        ball_color = [random.randint(0, 255) for _ in range(3)]

    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, ball_color, ball_pos, ball_radius)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()