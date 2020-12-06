import pygame
from pygame.locals import *

pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)


def get_sounds():
    sounds = {"circle": pygame.mixer.Sound("assets/sounds/button_click.wav"),
              "click": pygame.mixer.Sound("assets/sounds/circle_placed.wav")}
    return sounds
