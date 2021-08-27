import pygame

import variables


class Tile:

    def __init__(self, pos, color):
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.img = pygame.Surface((variables.TILE_SIZE, variables.TILE_SIZE))
        self.img.fill(color)
