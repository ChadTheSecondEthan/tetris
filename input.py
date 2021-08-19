import pygame


def update():

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        print("SPACE")
    if keys[pygame.K_LEFT]:
        print("LEFT")
    if keys[pygame.K_RIGHT]:
        print("RIGHT")
    if keys[pygame.K_DOWN]:
        print("DOWN")
    if keys[pygame.K_UP]:
        print("UP")