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
tiles = []

won = False

prev_time = 0
prev_block_time = 0
wait = 1.0 / variables.FPS


def start(s):
    global prev_time, background, screen, prev_block_time, current_block

    prev_time = time()
    prev_block_time = time()

    screen = s

    background = pygame.Surface(variables.SCREEN_SIZE)
    background = background.convert()

    get_new_block()


def update():
    global prev_time, prev_block_time

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()

    pygame.keydown = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            pygame.keydown = True
    input.update()

    if time() - prev_block_time > 1.0 / variables.FPS:
        current_block.update()
        prev_block_time = time()

    background.fill(variables.BG_COLOR)

    current_block.draw_preview(background)
    for _tile in tiles:
        background.blit(_tile.img, (_tile.x, _tile.y))
    if stored_block:
        for _tile in stored_block.tiles:
            background.blit(_tile.img, (_tile.x, _tile.y))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    prev_time = time()


def get_new_block():
    global current_block, stored_this_block
    current_block = block.spawn_random_block()

    if len(blocks) > 1 and blocks[-1] is not current_block:
        for tile in blocks[-1].tiles:
            if current_block.collides_with(tile):
                current_block = None
                return

    blocks.append(current_block)
    tiles.extend(current_block.tiles)
    stored_this_block = False


def try_remove_row():
    block_removed = False

    # get all y values of tiles
    y_values = []
    for tile in tiles:
        if tile.y not in y_values:
            y_values.append(tile.y)

    for y in y_values:
        num_tiles = 0
        for tile in tiles:
            if tile.y == y:
                num_tiles += 1
                if num_tiles == variables.TILE_X:
                    block_removed = True
                    for _tile in [] + tiles:
                        if _tile.y == y:
                            tiles.remove(_tile)
                        if _tile.y < y:
                            _tile.y += variables.TILE_SIZE
                    break
    if block_removed:
        try_remove_row()


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

    stored_block.set_position((2 * variables.TILE_SIZE, 2 * variables.TILE_SIZE))

    blocks.append(current_block)
    for tile in current_block.tiles:
        tiles.append(tile)

    blocks.remove(stored_block)
    for tile in stored_block.tiles:
        tiles.remove(tile)
