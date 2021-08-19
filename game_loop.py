import pygame
import sys
from time import perf_counter

import variables
import text


background: pygame.Surface
screen: pygame.display
entities = []
flags_text: text.Text
won = False
playing = True

prev_time: float


def start(s):
    global prev_time, background, screen, flags_text

    prev_time = perf_counter()

    screen = s

    background = pygame.Surface(variables.SCREEN_SIZE)
    background = background.convert()

    flags_text = text.Text("Flags: ", 10, 10)
    entities.append(flags_text)


def update():
    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    global prev_time, flags_text
    dt = perf_counter() - prev_time

    if playing:
        for entity in entities:
            entity.update(dt)

    background.fill(variables.BG_COLOR)

    for entity in entities:
        background.blit(entity.img, (entity.x, entity.y))

    screen.blit(background, (0, 0))
    pygame.display.flip()

    prev_time = perf_counter()
