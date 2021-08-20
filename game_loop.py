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
stored_this_block = False
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
        if event.type == pygame.KEYDOWN and playing:
            input.update()

    if playing and time() - prev_block_time > wait:
        current_block.update()
        prev_block_time = time()

    background.fill(variables.BG_COLOR)

    for b in blocks:
        if b is not stored_block:
            b.draw(background)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    prev_time = time()


def get_new_block():
    global current_block, stored_this_block
    current_block = block.spawn_random_block()

    if current_block.collides_with(blocks[-1]):
        current_block = None
        return

    blocks.append(current_block)
    stored_this_block = False


def try_remove_row():
    # TODO
    pass


def store_current_block():
    global stored_block, current_block, stored_this_block

    if stored_this_block:
        return

    stored_this_block = True
    tmp = current_block
    if stored_block is not None:
        current_block = stored_block
        current_block.reset_position()
        stored_block = tmp
    else:
        stored_block = current_block
        current_block = block.spawn_random_block()
    blocks.append(current_block)
    blocks.remove(stored_block)
