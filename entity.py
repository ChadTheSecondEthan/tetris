import pygame


class Entity:

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.Surface((w, h)).convert()
        self.img.fill((255, 255, 255))

    def update(self, dt):
        pass

    def set_color(self, color):
        self.img.fill(color)

    def intersects(self, other):
        return self.x + self.w > other.x and self.x < other.x + other.w \
               and self.y + self.h > other.y and self.y < other.y + other.h

    def intersects_point(self, point):
        return self.x + self.w > point[0] > self.x and self.y + self.h > point[1] > self.y

    def sqr_dist(self, other):
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2
