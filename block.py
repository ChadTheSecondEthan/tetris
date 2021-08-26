import sys
from random import random
import pygame

import variables
import game_loop

spawn_location = variables.TILE_X * variables.TILE_SIZE // 2, variables.TILE_SIZE * 3
frames_to_lock = 5
blocks = [
    ((130, 200, 255), ((0, -1), (0, 0), (0, 1), (0, 2)), ((-1, 0), (0, 0), (1, 0), (2, 0)),         # tall blue
     ((0, 1), (0, 0), (0, -1), (0, -2)), ((1, 0), (0, 0), (-1, 0), (-2, 0))),
    ((0, 0, 255), ((-1, -1), (-1, 0), (0, 0), (1, 0)), ((1, -1), (0, -1), (0, 0), (0, 1)),          # blue L
     ((1, 1), (-1, 0), (0, 0), (1, 0)), ((-1, 1), (0, 1), (0, 0), (0, -1))),
    ((255, 165, 0), ((1, -1), (-1, 0), (0, 0), (1, 0)), ((0, -1), (1, 1), (0, 0), (0, 1)),        # orange L
     ((-1, 1), (-1, 0), (0, 0), (1, 0)), ((-1, -1), (0, 1), (0, 0), (0, -1))),
    ((0, 255, 0), ((-1, 1), (0, 1), (0, 0), (1, 0)), ((-1, -1), (-1, 0), (0, 0), (0, 1)),           # green z
     ((-1, 1), (0, 1), (0, 0), (1, 0)), ((-1, -1), (-1, 0), (0, 0), (0, 1))),
    ((255, 0, 0), ((1, 1), (0, 1), (0, 0), (-1, 0)), ((1, -1), (1, 0), (0, 0), (0, 1)),             # red z
     ((1, 1), (0, 1), (0, 0), (-1, 0)), ((1, -1), (1, 0), (0, 0), (0, 1))),
    ((112, 51, 173), ((-1, 0), (0, -1), (0, 0), (1, 0)), ((0, -1), (1, 0), (0, 0), (0, 1)),       # purple t
     ((-1, 0), (0, 1), (0, 0), (1, 0)), ((0, -1), (-1, 0), (0, 0), (0, 1)))
]


class Block:

    def __init__(self, _type):
        self.rotation = 0
        self.frames_collided = 0
        self.images = []
        self.tiles = []
        self._type = _type
        self.blocks_moved = [0, 0]
        data = blocks[_type]
        for tile in self.get_tiles():
            img = pygame.Surface((variables.TILE_SIZE, variables.TILE_SIZE))
            img.fill(data[0])
            self.images.append(img)

            self.tiles.append([tile[0] * variables.TILE_SIZE + spawn_location[0],
                               tile[1] * variables.TILE_SIZE + spawn_location[1]])

        if self.check_block_collisions():
            print("Game over")
            sys.exit()

    def get_tiles(self):
        return blocks[self._type][1 + self.rotation]

    def move_up(self):
        for tile in self.tiles:
            tile[1] -= variables.TILE_SIZE

    def move_down(self):
        for tile in self.tiles:
            tile[1] += variables.TILE_SIZE

    def update(self):
        self.blocks_moved[1] += 1
        self.move_down()

        colliding = self.check_block_collisions()
        on_screen = self.v_on_screen()

        if colliding or not on_screen:
            self.frames_collided += 1
            self.move_up()

            if self.frames_collided >= frames_to_lock:
                if not on_screen:
                    self.move_down()
                game_loop.get_new_block()
                game_loop.try_remove_row()
                return
        else:
            self.frames_collided = 0

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

    def h_move(self, right, check=True):

        for _tile in self.tiles:
            if (not right and _tile[0] == 0) or \
               (right and _tile[0] == (variables.TILE_X - 1) * variables.TILE_SIZE):
                return

        self.blocks_moved[0] += 1 if right else -1

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
        self.rotation += 1 if right else -1
        if self.rotation == -1:
            self.rotation = 3
        else:
            self.rotation %= 4

        tmp_tiles = self.get_tiles()
        for i in range(len(self.tiles)):
            self.tiles[i] = [(tmp_tiles[i][0] + self.blocks_moved[0]) * variables.TILE_SIZE + spawn_location[0],
                             (tmp_tiles[i][1] + self.blocks_moved[1]) * variables.TILE_SIZE + spawn_location[1]]

        if self.check_block_collisions() or not self.v_on_screen():
            self.frames_collided = 0
            while True:
                if self.check_block_collisions() or not self.v_on_screen():
                    self.move_up()
                    self.blocks_moved[1] -= 1
                elif self.v_on_screen():
                    return

    def reset_position(self):
        self.tiles = []
        for tile in self.get_tiles():
            self.tiles.append([tile[0] * variables.TILE_SIZE + spawn_location[0],
                               tile[1] * variables.TILE_SIZE + spawn_location[1]])

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
