from random import random
import pygame

import variables
import game_loop

SPAWN_LOCATION = variables.WIDTH / 2, variables.TILE_SIZE * 3
blocks = [
    ((130, 200, 255), [(-1, -1), (-1, 0), (-1, 1), (-1, 2)]),   # tall blue
    ((0, 0, 255), [(-1, -1), (-1, 0), (0, 0), (1, 0)]),         # blue L
    ((255, 165, 0), [(1, -1), (-1, 0), (0, 0), (1, 0)]),        # orange L
    ((0, 255, 0), [(-1, 1), (0, 1), (0, 0), (1, 0)]),           # green z
    ((255, 0, 0), [(1, 1), (0, 1), (0, 0), (-1, 0)]),           # red z
    ((112, 51, 173), [(-1, 1), (0, 0), (0, 1), (1, 1)])         # purple t
]


class Block:

    def __init__(self, _type):
        self.images = []
        self.locations = []
        self._type = _type
        data = blocks[_type]
        for block in data[1]:
            img = pygame.Surface((variables.TILE_SIZE, variables.TILE_SIZE))
            img.fill(data[0])
            self.images.append(img)

            self.locations.append([block[0] * variables.TILE_SIZE + SPAWN_LOCATION[0],
                                   block[1] * variables.TILE_SIZE + SPAWN_LOCATION[1]])

        if self.check_collisions():
            game_loop.playing = False

    def update(self):
        for location in self.locations:
            location[1] += variables.TILE_SIZE
        if self.check_collisions():
            game_loop.get_new_block()
            if self.on_screen():
                for location in self.locations:
                    location[1] -= variables.TILE_SIZE
            game_loop.try_remove_row()

    def draw(self, bg):
        for i in range(len(self.images)):
            bg.blit(self.images[i], self.locations[i])

    def check_collisions(self):
        if not self.on_screen():
            return True

        for block in game_loop.blocks:
            if block is not self:
                if self.collides_with(block):
                    return True
        return False

    def on_screen(self):
        for location in self.locations:
            if location[1] > variables.HEIGHT - variables.TILE_SIZE - 1:
                return False
        return True

    def h_move(self, right, check=True):
        for location in self.locations:
            location[0] += variables.TILE_SIZE if right else -variables.TILE_SIZE
        if check and self.check_collisions():
            self.h_move(not right, check=False)

    def v_move(self, up):
        if up: # immediately fall
            while self is game_loop.current_block:
                self.update()
        else: # fall one tile faster
            # self.update()
            return

    def reset_position(self):
        self.locations = []
        for block in blocks[self._type][1]:
            self.locations.append([block[0] * variables.TILE_SIZE + SPAWN_LOCATION[0],
                                   block[1] * variables.TILE_SIZE + SPAWN_LOCATION[1]])

    def collides_with(self, other):
        for location in self.locations:
            for _location in other.locations:
                if location[0] == _location[0] and location[1] == _location[1]:
                    return True
        return False


def spawn_random_block():
    return Block(int(random() * len(blocks)))
