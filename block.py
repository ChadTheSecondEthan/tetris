import sys
from random import random
import pygame

import variables
import game_loop
from tile import Tile

spawn_location = variables.TILE_X * variables.TILE_SIZE // 2, variables.TILE_SIZE * 3
frames_to_lock = 5
blocks = [
    ((130, 200, 255), ((0, -1), (0, 0), (0, 1), (0, 2)), ((-1, 0), (0, 0), (1, 0), (2, 0)),  # tall blue
     ((0, 1), (0, 0), (0, -1), (0, -2)), ((1, 0), (0, 0), (-1, 0), (-2, 0))),
    ((0, 0, 255), ((-1, -1), (-1, 0), (0, 0), (1, 0)), ((1, -1), (0, -1), (0, 0), (0, 1)),  # blue L
     ((1, 1), (-1, 0), (0, 0), (1, 0)), ((-1, 1), (0, 1), (0, 0), (0, -1))),
    ((255, 165, 0), ((1, -1), (-1, 0), (0, 0), (1, 0)), ((0, -1), (1, 1), (0, 0), (0, 1)),  # orange L
     ((-1, 1), (-1, 0), (0, 0), (1, 0)), ((-1, -1), (0, 1), (0, 0), (0, -1))),
    ((0, 255, 0), ((-1, 1), (0, 1), (0, 0), (1, 0)), ((-1, -1), (-1, 0), (0, 0), (0, 1)),  # green z
     ((-1, 1), (0, 1), (0, 0), (1, 0)), ((-1, -1), (-1, 0), (0, 0), (0, 1))),
    ((255, 0, 0), ((1, 1), (0, 1), (0, 0), (-1, 0)), ((1, -1), (1, 0), (0, 0), (0, 1)),  # red z
     ((1, 1), (0, 1), (0, 0), (-1, 0)), ((1, -1), (1, 0), (0, 0), (0, 1))),
    ((112, 51, 173), ((-1, 0), (0, -1), (0, 0), (1, 0)), ((0, -1), (1, 0), (0, 0), (0, 1)),  # purple t
     ((-1, 0), (0, 1), (0, 0), (1, 0)), ((0, -1), (-1, 0), (0, 0), (0, 1))),
    ((255, 255, 0), ((-1, 0), (0, 0), (-1, 1), (0, 1)), ((-1, 0), (0, 0), (-1, 1), (0, 1)), # yellow square
     ((-1, 0), (0, 0), (-1, 1), (0, 1)), ((-1, 0), (0, 0), (-1, 1), (0, 1)))
]


class Block:

    def __init__(self, _type, check_collisions=True):
        self.rotation = 0
        self.frames_collided = 0
        self.images = []
        self.tiles = []
        self._type = _type
        self.blocks_moved = [0, 0]
        data = blocks[_type]
        for _tile in self.get_tiles():
            img = pygame.Surface((variables.TILE_SIZE, variables.TILE_SIZE))
            img.fill(data[0])
            self.images.append(img)

            self.tiles.append(Tile([_tile[0] * variables.TILE_SIZE + spawn_location[0],
                                    _tile[1] * variables.TILE_SIZE + spawn_location[1]], data[0]))

        if check_collisions and self.check_block_collisions():
            print("Game over")
            sys.exit()

    def get_tiles(self):
        return blocks[self._type][1 + self.rotation]

    def move_up(self):
        for tile in self.tiles:
            tile.y -= variables.TILE_SIZE

    def move_down(self):
        for tile in self.tiles:
            tile.y += variables.TILE_SIZE

    def move_left(self):
        for tile in self.tiles:
            tile.x -= variables.TILE_SIZE

    def move_right(self):
        for tile in self.tiles:
            tile.x += variables.TILE_SIZE

    def update(self):
        self.blocks_moved[1] += 1
        self.move_down()

        colliding = self.check_block_collisions()
        on_screen = self.v_on_screen()

        if colliding or not on_screen:
            self.frames_collided += 1
            self.move_up()

            if self.v_on_screen() and not colliding:
                self.move_down()

            if self.frames_collided >= frames_to_lock:
                if on_screen and not colliding:
                    self.move_down()
                game_loop.try_remove_row()
                game_loop.get_new_block()
                return True
        else:
            self.frames_collided = 0
        return False

    def check_block_collisions(self):
        for _tile in game_loop.tiles:
            if self.collides_with(_tile):
                return True
        return False

    def v_on_screen(self):
        for tile in self.tiles:
            if tile.y > variables.HEIGHT - variables.TILE_SIZE - 1:
                return False
        return True

    def h_on_screen(self):
        for tile in self.tiles:
            if tile.x < 0 or tile.x > variables.WIDTH - variables.TILE_SIZE:
                return False
        return True

    def h_move(self, right, check=True):
        for _tile in self.tiles:
            if (not right and _tile.x == 0) or \
                    (right and _tile.x == (variables.TILE_X - 1) * variables.TILE_SIZE):
                return

        self.blocks_moved[0] += 1 if right else -1

        for tile in self.tiles:
            tile.x += variables.TILE_SIZE if right else -variables.TILE_SIZE

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
        for _tile in self.tiles:
            game_loop.tiles.remove(_tile)
        for i in range(len(self.tiles)):
            self.tiles[i] = Tile([(tmp_tiles[i][0] + self.blocks_moved[0]) * variables.TILE_SIZE + spawn_location[0],
                                  (tmp_tiles[i][1] + self.blocks_moved[1]) * variables.TILE_SIZE + spawn_location[1]],
                                 self.tiles[0].color)
            game_loop.tiles.append(self.tiles[i])

        if self.check_block_collisions() or not self.v_on_screen() or not self.h_on_screen():
            self.frames_collided = 0
            while True:
                if self.check_block_collisions() or not self.v_on_screen():
                    self.move_up()
                    self.blocks_moved[1] -= 1
                elif self.v_on_screen():
                    break
            while True:
                moved = False
                for _tile in self.tiles:
                    if _tile.x > variables.WIDTH - variables.TILE_SIZE:
                        self.move_left()
                        moved = True
                        break
                if not moved:
                    break
            while True:
                moved = False
                for _tile in self.tiles:
                    if _tile.x <= 0:
                        self.move_right()
                        moved = True
                        break
                if not moved:
                    break

    def reset_position(self):
        color = self.tiles[0].color
        self.tiles = []
        for tile in self.get_tiles():
            self.tiles.append(Tile([tile[0] * variables.TILE_SIZE + spawn_location[0],
                                    tile[1] * variables.TILE_SIZE + spawn_location[1]], color))

    def set_position(self, pos):
        start_positions = blocks[self._type][1]
        for i in range(len(self.tiles)):
            self.tiles[i].x = pos[0] + start_positions[i][0] * variables.TILE_SIZE
            self.tiles[i].y = pos[1] + start_positions[i][1] * variables.TILE_SIZE

    def collides_with(self, tile):
        for _tile in self.tiles:
            if _tile is tile:
                return False
            if tile.x == _tile.x and tile.y == _tile.y:
                return True
        return False

    def draw_preview(self, background):
        preview_block = Block(self._type, check_collisions=False)
        for i in range(len(preview_block.tiles)):
            preview_block.tiles[i].x = self.tiles[i].x
            preview_block.tiles[i].y = self.tiles[i].y
        should_run = True
        while should_run and preview_block.v_on_screen():
            for tile in preview_block.tiles:
                tile.y += variables.TILE_SIZE
            for tile in game_loop.tiles:
                if tile not in self.tiles and tile not in preview_block.tiles and preview_block.collides_with(tile):
                    for _tile in preview_block.tiles:
                        _tile.y -= variables.TILE_SIZE
                    should_run = False
        for i in range(len(preview_block.tiles)):
            preview_block.tiles[i].img.fill((255, 255, 255))
            background.blit(preview_block.tiles[i].img, (preview_block.tiles[i].x, preview_block.tiles[i].y))


def spawn_random_block():
    return Block(int(random() * len(blocks)))
