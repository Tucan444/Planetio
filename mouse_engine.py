import math
from fast_and_trash import *
import pygame


class Mouse:

    points = 0

    def __init__(self, mouse_pos):
        self.mouse_pos = mouse_pos

    def update(self, Win_size, Default_size):
        self.mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = [round(self.mouse_pos[0] * (Default_size[0] / Win_size[0])),
                          round(self.mouse_pos[1] * (Default_size[1] / Win_size[1]))]

    def in_circle(self, circle_cords, radius):
        if distance_indicator(self.mouse_pos, circle_cords) < radius:
            return True
        else:
            return False

    def check_availability(self, color_name, radius, game, scroll):
        scrolled_pos = [self.mouse_pos[0] + scroll.scroll[0],
                        self.mouse_pos[1] + scroll.scroll[1]]

        collided = []
        for circle in game.circles:
            dist = distance_indicator(circle.center, scrolled_pos)

            if dist < (radius + circle.radius):
                if dist < radius or dist < circle.radius:
                    return False
                collided.append(circle)

        if collided:

            # if u try placing red circle
            if color_name == "red":
                for circle in collided:
                    if circle.color == "purple":
                        return False

                return True

            # if u try placing blue circle
            if color_name == "blue":
                usable = False

                for circle in collided:
                    if circle.color not in ["black", "smaragd", "red"]:
                        return False
                    else:
                        usable = True

                if usable:
                    return True
                else:
                    return False

            # if u try placing green circle
            if color_name == "green":
                usable = [False, False]

                for circle in collided:
                    if circle.color not in ["black", "smaragd", "red", "blue"]:
                        return False
                    elif circle.color in ["black", "smaragd"]:
                        usable = [True, True]
                    elif circle.color == "red":
                        usable[0] = True
                    else:
                        usable[1] = True

                if usable[0] and usable[1]:
                    return True
                else:
                    return False

            # if u try placing yellow circle
            if color_name == "yellow":
                usable = [False, False]
                for circle in collided:
                    if circle.color not in ["red", "green", "black", "smaragd"]:
                        return False
                    elif circle.color in ["black", "smaragd"]:
                        usable = [True, True]
                    elif circle.color == "red":
                        usable[0] = True
                    else:
                        usable[1] = True

                if usable[0] and usable[1]:
                    return True
                else:
                    return False

            # if u try placing purple circle
            if color_name == "purple":
                usable = [False, False, False, False]
                for circle in collided:
                    if circle.color not in ["red", "blue", "green", "yellow", "black", "smaragd"]:
                        return False
                    elif circle.color in ["black", "smaragd"]:
                        usable = [True, True, True, True]
                    elif circle.color == "red":
                        usable[0] = True
                    elif circle.color == "blue":
                        usable[1] = True
                    elif circle.color == "green":
                        usable[2] = True
                    else:
                        usable[3] = True

                if usable[0] and usable[1] and usable[2] and usable[3]:
                    return True
                else:
                    return False

            # if u try placing smaragd circle
            if color_name == "smaragd":
                usable = False
                for circle in collided:
                    if circle.color not in ["purple", "black"]:
                        return False
                    else:
                        usable = True

                if usable:
                    return True
                else:
                    return False
        else:
            return False
