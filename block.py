from random import random
import pygame

import variables

SPAWN_LOCATION = variables.WIDTH / 2, 50
blocks = [
    ((130, 200, 255), [(-1, -1), (-1, 0), (-1, 1), (-1, 2)])
]


class Block:

    def __init__(self, _type):
        self.images = []
        self.locations = []
        data = blocks[_type]
        for block in data[1]:
            img = pygame.Surface((variables.TILE_SIZE, variables.TILE_SIZE))
            img.fill(data[0])
            self.images.append(img)

            self.locations.append((block[0] * variables.TILE_SIZE + SPAWN_LOCATION[0],
                                   block[1] * variables.TILE_SIZE + SPAWN_LOCATION[1]))

    def update(self):
        for i in range(len(self.locations)):
            self.locations[i] = #TODO

    def draw(self, bg):
        for i in range(len(self.images)):
            bg.blit(self.images[i], self.locations[i])


def spawn_random_block():
    return Block(int(random() * len(blocks)))
