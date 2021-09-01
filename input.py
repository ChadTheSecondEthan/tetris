import pygame

import game_loop
import variables

fast_fall_block = None


def update():
    global fast_fall_block
    keys = pygame.key.get_pressed()

    if game_loop.current_block is None:
        return

    if pygame.keydown:
        if keys[pygame.K_SPACE]:
            game_loop.store_current_block()

        if keys[pygame.K_LEFT]:
            game_loop.current_block.h_move(False)
        if keys[pygame.K_RIGHT]:
            game_loop.current_block.h_move(True)
        if keys[pygame.K_UP]:
            game_loop.current_block.v_move(True)

        if keys[pygame.K_a]:
            game_loop.current_block.rotate(False)
        if keys[pygame.K_d]:
            game_loop.current_block.rotate(True)
    if keys[pygame.K_DOWN]:
        if game_loop.current_block is fast_fall_block:
            variables.FPS = 15
    else:
        fast_fall_block = game_loop.current_block
        variables.FPS = 6
