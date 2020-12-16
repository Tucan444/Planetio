import json
import math
import random
import pygame
from pygame.locals import *

pygame.init()


def distance_indicator(cords1, cords2):
    x_distance = abs(cords1[0] - cords2[0])
    y_distance = abs(cords1[1] - cords2[1])
    distance = math.sqrt((x_distance ** 2) + (y_distance ** 2))
    return round(distance, 4)


def area_intersection_of_circles(points, radius_list):
    try:
        dist = distance_indicator(points[0], points[1])

        alpha_cos = (pow(radius_list[1], 2) + pow(dist, 2) - pow(radius_list[0], 2)) / (2 * radius_list[1] * dist)

        alpha = math.acos(alpha_cos)

        beta_cos = (dist - alpha_cos * radius_list[1]) / radius_list[0]

        beta = math.acos(beta_cos)

        triangles = (alpha_cos * pow(radius_list[1], 2) * math.sin(alpha)) + (
                beta_cos * pow(radius_list[0], 2) * math.sin(beta))

        arcs = ((math.pi * pow(radius_list[0], 2) * beta * 2) / math.tau) + (
                (math.pi * pow(radius_list[1], 2) * alpha * 2) / math.tau)

        return arcs - triangles
    except:
        return False


class Circle:
    def __init__(self, radius, center, colorX, color_value):
        self.radius = radius
        self.center = center
        self.color = colorX
        self.color_value = color_value

    def draw(self, display, scroll):
        sur = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(sur, self.color_value, [self.radius, self.radius], self.radius)
        sur.set_alpha(self.color_value.a)
        sur.set_colorkey((0, 0, 0))
        display.blit(sur, [-self.radius + self.center[0] - scroll.scroll[0],
                           -self.radius + self.center[1] - scroll.scroll[1]])


class Game:
    def __init__(self):
        self.alive = True
        self.circles = []
        self.c_template = {"color": "red",
                           "radius": random.randint(30, 50),
                           "pos": pygame.mouse.get_pos()}
        self.colors = get_colors()
        self.color_names = list(self.colors.keys())
        self.ended_on_own_will = False

        # scroll
        self.aditional_scroll = [0, 0]

        # consts
        self.midpoint = [450, 300]

        # for gravity
        self.base_limit = 1000
        self.limit = 1000
        self.black = None
        self.collapse = False

        # points
        self.points = 0

    def add_circle(self, pos, radius, colorX, color_value, scroll):
        new_pos = [pos[0] + scroll.scroll[0], pos[1] + scroll.scroll[1]]
        self.circles.append(Circle(radius, new_pos, colorX, color_value))

    def disp_circles(self, display, scroll):
        for circle in self.circles:
            circle.draw(display, scroll)

    def get_new_circle_template(self):
        self.c_template = get_circle_template(self.color_names)

    def draw_template(self, display):
        sur = pygame.Surface((self.c_template["radius"] * 2, self.c_template["radius"] * 2))
        pygame.draw.circle(sur, self.colors[self.c_template["color"]],
                           [self.c_template["radius"],
                            self.c_template["radius"]], self.c_template["radius"])
        sur.set_alpha(self.colors[self.c_template["color"]].a)
        sur.set_colorkey((0, 0, 0))
        display.blit(sur, [-self.c_template["radius"] + self.c_template["pos"][0],
                           -self.c_template["radius"] + self.c_template["pos"][1]])

    def get_gravity(self):
        final_value = [0, 0]

        for circle in self.circles:
            dist = distance_indicator(circle.center, self.midpoint)
            angle = find_angle_between_points(circle.center, self.midpoint)
            final_value[0] += round(math.cos(angle) * dist, 2) * (circle.radius / 20)
            final_value[1] += round(math.sin(angle) * dist, 2) * (circle.radius / 20)

        dist = distance_indicator(self.midpoint, [final_value[0] + self.midpoint[0], final_value[1] + self.midpoint[1]])
        if dist > self.limit:
            self.collapse = True
            self.alive = False

        elif dist > self.limit * 0.6:
            self.black.color_value.r = round((dist - (self.limit * 0.6)) * (255 / (self.limit * 0.4)))
            if self.black.color_value.r > 255:
                self.black.color_value.r = 255

        else:
            self.black.color_value.r = 0

        return final_value

    # must be called before add circle
    def update_points(self, pos, radius, colorX):
        collided = []
        multiplier = 1
        for circle in self.circles:
            dist = distance_indicator(circle.center, pos)

            if dist < (radius + circle.radius):
                collided.append(circle)

        for circle in collided:
            area = area_intersection_of_circles([pos, circle.center], [circle.radius, radius])

            if colorX == "green":
                multiplier = 1.1
            elif colorX == "yellow":
                multiplier = 1.2
            elif colorX == "purple":
                multiplier = 2
            elif colorX == "smaragd":
                multiplier = 4

            self.points += (area // 10) * multiplier

    def update_lim(self):
        self.limit = self.base_limit + (self.points / 10)

    def rotate_around_mid(self):
        for circle in self.circles:
            if circle.color != "black":
                dist = distance_indicator(circle.center, self.midpoint)
                angle = find_angle_between_points(self.midpoint, circle.center)
                angle -= 0.005
                angle = round(angle, 3)
                circle.center = [self.midpoint[0] + (math.cos(angle) * dist),
                                 self.midpoint[1] + (math.sin(angle) * dist)]

    # saving & loading
    def save(self, path, setup):

        save = {"gravity": setup["gravity"],
                "next_circle": self.c_template,
                "limit": self.limit,
                "points": self.points,
                "circles": []}

        for circle in self.circles:
            save["circles"].append({"radius": circle.radius,
                                    "center": circle.center,
                                    "color": circle.color,
                                    "color_value": str(circle.color_value)})

        del save["circles"][0]

        with open(path, "w") as f:
            json.dump(save, f, indent=4)

    def load(self, path, setup):

        with open(path, "r") as f:
            save = json.load(f)

        setup["gravity"] = save["gravity"]

        self.c_template = save["next_circle"]

        for circle in save["circles"]:
            self.circles.append(Circle(circle["radius"], circle["center"], circle["color"],
                                       pygame.Color(eval(circle["color_value"]))))

        self.points = save["points"]
        self.limit = save["limit"]

        return setup


class Scroll:
    def __init__(self, scroll):
        self.scroll = scroll
        self.fade = 20
        self.safe_fade = 20
        self.in_progress = False
        self.save_scroll = self.scroll

    def move_scroll(self, player, screen, which, space=20):
        if which == "y" or which == "both":
            self.scroll[1] += (player.rect.y - self.scroll[1] - (screen[1] / 2) + (player.size[1] / 2)) / space
            self.scroll[1] = int(self.scroll[1])
        if which == "x" or which == "both":
            self.scroll[0] += (player.rect.x - self.scroll[0] - (screen[0] / 2) + (player.size[0] / 2)) / space
            self.scroll[0] = int(self.scroll[0])

    def add_scroll(self, which, how_much, fade=None):
        if fade is not None:
            self.safe_fade = fade
            if self.in_progress is False:
                self.load_safe_fade()
                self.save_scroll = self.scroll
                self.in_progress = True
            how_much[0] /= self.fade
            how_much[1] /= self.fade
            self.fade += 0.01 * self.fade

        if which == "x" or which == "both":
            self.scroll[0] += how_much[0]
            self.scroll[0] = round(self.scroll[0])

        if which == "y" or which == "both":
            self.scroll[1] += how_much[1]
            self.scroll[1] = round(self.scroll[1])

    def load_safe_fade(self):
        self.fade = self.safe_fade
        self.in_progress = False


def get_colors():
    colors = {"red": pygame.Color(255, 0, 0, 125),  # weight 16
              "blue": pygame.Color(0, 0, 220, 125),  # weight 20
              "green": pygame.Color(0, 220, 0, 125),  # weight 20
              "yellow": pygame.Color(252, 239, 56, 125),  # weight 22
              "purple": pygame.Color(105, 0, 158, 125),  # weight 4
              "smaragd": pygame.Color(0, 214, 168, 125)}  # weight 1
    return colors


def get_random_color():
    colors = []
    colors = add_to_list("red", 20, colors)
    colors = add_to_list("blue", 20, colors)
    colors = add_to_list("green", 20, colors)
    colors = add_to_list("yellow", 18, colors)
    colors = add_to_list("purple", 4, colors)
    colors = add_to_list("smaragd", 1, colors)
    return colors[random.randint(0, len(colors) - 1)]


def get_circle_template():
    template = {"color": get_random_color(),
                "radius": random.randint(10, 50),
                "pos": pygame.mouse.get_pos()}
    return template


def add_to_list(what, amount, listx):
    for i in range(amount):
        listx.append(what)
    return listx


def find_angle_between_points(center, point):
    dists = distances(center, point)
    try:
        angle = math.atan(dists[1] / dists[0])

        if point[0] < center[0]:
            if point[1] < center[1]:
                return angle + math.pi
            else:
                return (math.pi / 2 - angle) + (math.pi / 2)
        else:
            if point[1] < center[1]:
                return (math.pi / 2 - angle) + 3 * (math.pi / 2)
            else:
                return angle
    except ZeroDivisionError:
        return False


def distances(cords1, cords2):
    return [abs(cords1[0] - cords2[0]), abs(cords1[1] - cords2[1])]


def get_circle(color_value, radius):
    sur = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(sur, color_value, [radius, radius], radius)
    sur.set_alpha(color_value.a)
    sur.set_colorkey((0, 0, 0))
    return sur


def get_gravity_sur(gravity, limit):
    ratio = limit / 40
    sur = pygame.Surface((100, 100))
    pygame.draw.circle(sur, (200, 200, 200), [50, 50], 40)
    pygame.draw.circle(sur, (217, 24, 114), [50 + (gravity[0] / ratio), 50 + (gravity[1] / ratio)], 10)
    sur.set_alpha(200)
    sur.set_colorkey((0, 0, 0))
    return sur


def rotate(center, pos, angleX):
    dist = distance_indicator(center, pos)
    angle = find_angle_between_points(center, pos)
    angle += angleX
    return [center[0] + (math.cos(angle) * dist), center[1] + (math.sin(angle) * dist)]
