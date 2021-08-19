import pygame

import variables
import game_loop

pygame.init()
pygame.font.init()


def main():
    screen = pygame.display.set_mode(variables.SCREEN_SIZE)
    pygame.display.set_caption("Tetris")

    run(screen)


def run(screen):
    game_loop.start(screen)

    # Event loop
    while True:
        game_loop.update()


if __name__ == "__main__":
    main()
