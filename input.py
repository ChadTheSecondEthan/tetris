import pygame

import game_loop


def update():
    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        print("SPACE")
    if keys[pygame.K_LEFT]:
        game_loop.current_block.h_move(False)
    if keys[pygame.K_RIGHT]:
        game_loop.current_block.h_move(True)
    if keys[pygame.K_DOWN]:
        game_loop.current_block.v_move(False)
    if keys[pygame.K_UP]:
        game_loop.current_block.v_move(True)