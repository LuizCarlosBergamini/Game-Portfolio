import pygame
from functools import cache


class Spritesheet:
    def __init__(self):
        pass

    def get_image(self, sheet, frame, width, height, scale, color, direction):
        image = pygame.Surface((width, height)).convert_alpha()
        image.fill(color)
        image.blit(sheet, (0, 0),
                   ((((frame * width) + (direction * width)), 0, width, height)))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)

        return image
