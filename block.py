import sys
from random import random
import pygame

import variables
import game_loop

SPAWN_LOCATION = variables.TILE_X * variables.TILE_SIZE / 2, variables.TILE_SIZE * 3
blocks = [
    ((130, 200, 255), [(0, -1), (0, 0), (0, 1), (0, 2)]),  # tall blue
    ((0, 0, 255), [(-1, -1), (-1, 0), (0, 0), (1, 0)]),  # blue L
    ((255, 165, 0), [(1, -1), (-1, 0), (0, 0), (1, 0)]),  # orange L
    ((0, 255, 0), [(-1, 1), (0, 1), (0, 0), (1, 0)]),  # green z
    ((255, 0, 0), [(1, 1), (0, 1), (0, 0), (-1, 0)]),  # red z
    ((112, 51, 173), [(-1, 1), (0, 0), (0, 1), (1, 1)])  # purple t
]


class Block:

    def __init__(self, _type):
        self.images = []
        self.tiles = []
        self._type = _type
        data = blocks[_type]
        for block in data[1]:
            img = pygame.Surface((variables.TILE_SIZE, variables.TILE_SIZE))
            img.fill(data[0])
            self.images.append(img)

            self.tiles.append([block[0] * variables.TILE_SIZE + SPAWN_LOCATION[0],
                               block[1] * variables.TILE_SIZE + SPAWN_LOCATION[1]])

        if self.check_block_collisions():
            print("Game over")
            sys.exit()

    def update(self):
        for tile in self.tiles:
            tile[1] += variables.TILE_SIZE
        if self.check_block_collisions() or not self.v_on_screen():
            game_loop.get_new_block()
            if self.v_on_screen() or self.check_block_collisions():
                for location in self.tiles:
                    location[1] -= variables.TILE_SIZE
            game_loop.try_remove_row()

    def draw(self, bg):
        for i in range(len(self.images)):
            bg.blit(self.images[i], self.tiles[i])

    def check_block_collisions(self):
        for block in game_loop.blocks:
            if block is not self:
                if self.collides_with(block):
                    return True
        return False

    def v_on_screen(self):
        for tile in self.tiles:
            if tile[1] > variables.HEIGHT - variables.TILE_SIZE - 1:
                return False
        return True

    def h_on_screen(self):
        for tile in self.tiles:
            if tile[0] < 1 or tile[0] > variables.WIDTH - variables.TILE_SIZE - 1:
                return False
        return True

    def h_move(self, right, check=True):
        if self.h_on_screen():
            for tile in self.tiles:
                tile[0] += variables.TILE_SIZE if right else -variables.TILE_SIZE

        if check and self.check_block_collisions():
            self.h_move(not right, check=False)

    def v_move(self, up):
        if up:  # immediately fall
            while self is game_loop.current_block:
                self.update()
        else:  # fall one tile faster
            # self.update()
            return

    def rotate(self, right):
        dy = []
        tmp_tiles = []
        data = blocks[self._type]

        for i in range(len(data[1])):
            block = data[1][i]
            tmp = data[1][i][0], data[1][i][1]
            tmp_tiles.append([block[0] * variables.TILE_SIZE + SPAWN_LOCATION[0],
                              block[1] * variables.TILE_SIZE + SPAWN_LOCATION[1]])
            dy.append(self.tiles[i][1] - tmp_tiles[i][1])

        for tile in self.tiles:
            tmp = tile[0], tile[1]
            tile[0] = tmp[1] if right else -tmp[1]
            tile[1] = tile[1]

    def reset_position(self):
        self.tiles = []
        for block in blocks[self._type][1]:
            self.tiles.append([block[0] * variables.TILE_SIZE + SPAWN_LOCATION[0],
                               block[1] * variables.TILE_SIZE + SPAWN_LOCATION[1]])

    def set_position(self, pos):
        start_positions = blocks[self._type][1]
        for i in range(len(self.tiles)):
            self.tiles[i][0] = pos[0] + start_positions[i][0] * variables.TILE_SIZE
            self.tiles[i][1] = pos[1] + start_positions[i][1] * variables.TILE_SIZE

    def collides_with(self, other):
        for tile in self.tiles:
            for _tile in other.tiles:
                if tile[0] == _tile[0] and tile[1] == _tile[1]:
                    return True
        return False


def spawn_random_block():
    return Block(int(random() * len(blocks)))
    # return Block(0)
