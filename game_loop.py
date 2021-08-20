import pygame
import sys
from time import time

import block
import input
import variables


background = None
screen = None

stored_block = None
current_block = None
blocks = []

won = False
playing = True

prev_time = 0
prev_block_time = 0
wait = 1 / variables.FPS


def start(s):
    global prev_time, background, screen, prev_block_time, current_block

    prev_time = time()
    prev_block_time = time()

    screen = s

    current_block = block.spawn_random_block()
    blocks.append(current_block)

    background = pygame.Surface(variables.SCREEN_SIZE)
    background = background.convert()


def update():
    global prev_time, prev_block_time

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            input.update()

    if time() - prev_block_time > wait:
        current_block.update()
        prev_block_time = time()

    background.fill(variables.BG_COLOR)

    for b in blocks:
        b.draw(background)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    prev_time = time()
