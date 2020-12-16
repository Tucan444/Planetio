from Sounds import *
from mouse_engine import *
import pygame
import sys
from pygame.locals import *

# basic config
pygame.mixer.pre_init(48000, -16, 2, 512)
pygame.init()
pygame.mixer.set_num_channels(16)

font = pygame.font.SysFont('Comic Sans MS', 80)
small_font = pygame.font.SysFont('Comic Sans MS', 40)
tiny_font = pygame.font.SysFont('Comic Sans MS', 20)

Window_size = [900, 600]
Default_size = Window_size
monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
screen = pygame.display.set_mode(Window_size)
display = pygame.Surface((900, 600))
pygame.display.set_caption("Planetio")
pygame.display.set_icon(pygame.image.load("assets/textures/icon.png"))
clock = pygame.time.Clock()
sounds = get_sounds()


def menu(screenX, fs, Win_size):

    # preparations

    alive = True
    gravity_button = [pygame.image.load("assets/textures/gravity_not_nonhover.png").convert(),
                      pygame.image.load("assets/textures/gravity_not_hover.png").convert(),
                      pygame.image.load("assets/textures/gravity_do_nonhover.png").convert(),
                      pygame.image.load("assets/textures/gravity_do_hover.png").convert()]
    g_index = 0
    sheets = [pygame.image.load("assets/textures/sheet.png").convert(),
              pygame.image.load("assets/textures/sheet_cheat.png").convert(),
              pygame.image.load("assets/textures/sheet_pressed.png").convert(),
              pygame.image.load("assets/textures/sheet_cheat_pressed.png").convert()]
    sheets[0].set_colorkey((0, 0, 0))
    sheets[1].set_colorkey((0, 0, 0))
    sheets[2].set_colorkey((0, 0, 0))
    sheets[3].set_colorkey((0, 0, 0))
    s_index = 0

    load = [pygame.image.load("assets/textures/load.png").convert(),
            pygame.image.load("assets/textures/load_hover.png").convert()]
    for item in load:
        item.set_colorkey((0, 0, 0))
    l_index = 0

    # values to pass

    setup = {"rotate": True,
             "gravity": False,
             "cheatsheet": True,
             "load": False}

    # mouse

    mouse = Mouse([0, 0])
    colorX = (0, 0, 0)
    rotate_color = (0, 0, 0)
    r_circle_cords = [730, 500]

    # game loop
    while alive:
        display.fill((255, 255, 255))

        # event loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse.update(Win_size, Default_size)

                # setting actions for buttons
                if mouse.in_circle([200, 120], 50):
                    with open("assets/save.json", "r") as f:
                        file = json.load(f)

                    if file != {}:
                        setup["load"] = True
                    sounds["click"].play(0)
                    screenX, fs, Win_size = run_game(screenX, fs, setup, Win_size)

                    setup["load"] = False

                if mouse.in_circle([450, 300], 50):
                    sounds["click"].play(0)
                    screenX, fs, Win_size = run_game(screenX, fs, setup, Win_size)

                if mouse.in_circle([700, 500], 20):
                    sounds["click"].play(0)
                    setup["rotate"] = not setup["rotate"]

                if mouse.in_circle([107, 375], 17):
                    sounds["click"].play(0)
                    setup["gravity"] = not setup["gravity"]

                if mouse.in_circle([743, 140], 35):
                    sounds["click"].play(0)
                    setup["cheatsheet"] = not setup["cheatsheet"]

            if event.type == pygame.MOUSEMOTION:
                # if mouse moving get mouse pos
                mouse.update(Win_size, Default_size)

                if mouse.in_circle([450, 300], 50):
                    colorX = (100, 100, 100)
                else:
                    colorX = (0, 0, 0)

                if mouse.in_circle([700, 500], 20):
                    rotate_color = (80, 80, 80)
                else:
                    rotate_color = (0, 0, 0)

                if mouse.in_circle([107, 375], 17):
                    if setup["gravity"]:
                        g_index = 1
                    else:
                        g_index = 3
                else:
                    if setup["gravity"]:
                        g_index = 0
                    else:
                        g_index = 2

                if mouse.in_circle([743, 140], 35):
                    s_index = 1
                else:
                    s_index = 0

                if mouse.in_circle([200, 120], 50):
                    l_index = 1
                else:
                    l_index = 0

            if event.type == KEYDOWN:
                if event.key == K_f:
                    fs = not fs
                    if fs is False:
                        Win_size = Default_size
                        screenX = pygame.display.set_mode(Win_size)
                    else:
                        screenX = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        d = pygame.display.get_surface()
                        Win_size = [int((d.get_height() / 2) * 3), d.get_height()]

                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # making menu

        pygame.draw.circle(display, colorX, [450, 300], 50)

        pygame.draw.circle(display, rotate_color, [700, 500], 20)
        pygame.draw.circle(display, (126, 189, 43), r_circle_cords, 10)
        if setup["rotate"]:

            r_circle_cords = rotate([700, 500], r_circle_cords, -0.01)

        display.blit(gravity_button[g_index], [40, 300])

        # sheets

        if setup["cheatsheet"]:
            display.blit(sheets[1 + (s_index * 2)], [700, 100])
        else:
            display.blit(sheets[0 + (s_index * 2)], [700, 100])

        # load

        display.blit(load[l_index], [140, 60])

        # basic loop config

        screenX.blit(pygame.transform.scale(display, Win_size), (0, 0))
        pygame.display.update()
        clock.tick(60)


def run_game(screenX, fs, setup, Win_size):

    # basics
    mouse = Mouse([0, 0])
    mouse.update(Win_size, Default_size)
    game = Game()
    scroll = Scroll([0, 0])
    game.add_circle([450, 300], 40, "black", pygame.Color(10, 10, 10, 255), scroll)
    game.black = game.circles[0]

    # indicator
    indicator_colors = [pygame.Color(230, 73, 25, 150), pygame.Color(165, 230, 25, 150)]
    indicators = [get_circle(indicator_colors[0], 30), get_circle(indicator_colors[1], 30)]
    allowed = None

    # exit button
    exit_buttons = [get_circle(pygame.Color(1, 1, 1, 200), 20), get_circle(pygame.Color(255, 0, 0, 200), 20)]
    endex = 0

    # wasd tutorial
    wasd = pygame.image.load("assets/textures/wasd.png").convert()
    wasd.set_colorkey((0, 0, 0))
    wasd_timer = 0

    # cheatsheet
    cheatsheet = pygame.image.load("assets/textures/cheatsheet.png").convert()
    cheatsheet.set_colorkey((0, 0, 0))
    cheatsheet.set_alpha(180)

    # if loading
    if setup["load"]:
        setup = game.load("assets/save.json", setup)

    while game.alive:

        display.fill((255, 255, 255))

        # circles stuff

        game.disp_circles(display, scroll)
        game.draw_template(display)
        if setup["rotate"]:
            game.rotate_around_mid()

        # mouse checking
        mouse.update(Win_size, Default_size)

        game.c_template["pos"] = mouse.mouse_pos

        if setup["rotate"]:
            if mouse.check_availability(game.c_template["color"], game.c_template["radius"], game, scroll):
                allowed = True
            else:
                allowed = False

        # indicator & sensor

        if allowed:
            display.blit(indicators[1], [830, 530])
        else:
            display.blit(indicators[0], [830, 530])

        if setup["gravity"]:
            sensor = get_gravity_sur(game.get_gravity(), game.limit)

            display.blit(sensor, [10, 490])

        # exit button

        display.blit(exit_buttons[endex], [850, 10])

        # wasd tutorial

        if setup["cheatsheet"]:
            if wasd_timer < 255:
                wasd.set_alpha(255 - wasd_timer)
                wasd_timer += 2
                display.blit(wasd, [50, 260])

        # and cheatsheet

        if setup["cheatsheet"]:
            display.blit(cheatsheet, [0, 5])

        # scroll stuff

        scroll.scroll[0] += game.aditional_scroll[0]
        scroll.scroll[1] += game.aditional_scroll[1]

        # event loop

        for event in pygame.event.get():
            if event.type == QUIT:
                game.save("assets/save.json", setup)
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if mouse.check_availability(game.c_template["color"], game.c_template["radius"], game, scroll):
                    game.update_points([mouse.mouse_pos[0] + scroll.scroll[0],
                                        mouse.mouse_pos[1] + scroll.scroll[1]], game.c_template["radius"],
                                       game.c_template["color"])
                    # command above must run before u add circle

                    game.add_circle(mouse.mouse_pos, game.c_template["radius"], game.c_template["color"],
                                    game.colors[game.c_template["color"]], scroll)
                    game.c_template = get_circle_template()
                    sounds["circle"].play(0)

                    if setup["gravity"]:
                        game.update_lim()

                if mouse.in_circle([870, 30], 20):
                    game.alive = False
                    game.ended_on_own_will = True
                    sounds["click"].play(0)

            elif event.type == pygame.MOUSEMOTION:

                if setup["rotate"] is False:
                    if mouse.check_availability(game.c_template["color"], game.c_template["radius"], game, scroll):
                        allowed = True
                    else:
                        allowed = False

                if mouse.in_circle([870, 30], 20):
                    endex = 1
                else:
                    endex = 0

            elif event.type == KEYDOWN:
                if event.key == K_f:
                    fs = not fs
                    if fs is False:
                        Win_size = Default_size
                        screenX = pygame.display.set_mode(Win_size)
                    else:
                        screenX = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        d = pygame.display.get_surface()
                        Win_size = [int((d.get_height() / 2) * 3), d.get_height()]

                elif event.key == K_ESCAPE:
                    game.save("assets/save.json", setup)
                    return screenX, fs, Win_size

                elif event.key == K_r:
                    with open("assets/save.json", "w") as f:
                        json.dump({}, f, indent=4)
                    return screenX, fs, Win_size

                # managing scroll
                elif event.key == K_s:
                    game.aditional_scroll[1] += 10
                elif event.key == K_w:
                    game.aditional_scroll[1] -= 10
                elif event.key == K_a:
                    game.aditional_scroll[0] -= 10
                elif event.key == K_d:
                    game.aditional_scroll[0] += 10

            elif event.type == KEYUP:

                # just scroll
                if event.key == K_s:
                    game.aditional_scroll[1] -= 10
                elif event.key == K_w:
                    game.aditional_scroll[1] += 10
                elif event.key == K_a:
                    game.aditional_scroll[0] += 10
                elif event.key == K_d:
                    game.aditional_scroll[0] -= 10

        # basic loop config

        screenX.blit(pygame.transform.scale(display, Win_size), (0, 0))
        pygame.display.update()
        clock.tick(60)

    if game.collapse or game.ended_on_own_will:

        # setting up
        display.fill((255, 255, 255))
        if game.collapse:
            game.black.color_value.r = 255
        game.disp_circles(display, scroll)
        screenX.blit(pygame.transform.scale(display, Win_size), (0, 0))
        pygame.display.update()

        # todo save
        with open("assets/save.json", "w") as f:
            json.dump({}, f, indent=4)

        # ending
        if game.collapse:
            screenX, fs, Win_size = end(screenX, fs, Win_size, game, "collapse")
        else:
            screenX, fs, Win_size = end(screenX, fs, Win_size, game, "ignore")

    return screenX, fs, Win_size


def end(screenX, fs, Win_size, game, reason):
    # prep work

    game.alive = True
    mouse = Mouse([0, 0])
    mouse.update(Win_size, Default_size)

    # bg
    sur = pygame.Surface((800, 500))
    sur.fill((0, 0, 0))
    sur.set_alpha(20)
    display.blit(sur, [50, 50])

    # loading objects
    title = font.render("Game ended.", False, (40, 40, 40))
    reason_text = None
    if reason == "collapse":
        reason_text = tiny_font.render("planet collapsed", False, (40, 40, 40))

    circles = small_font.render(f"Circles placed : {len(game.circles)-1}", False, (40, 40, 40))
    points = small_font.render(f"Points collected : {round(game.points)}", False, (40, 40, 40))

    # menu button
    button_colors = [pygame.Color(60, 60, 60, 150), pygame.Color(160, 160, 160, 150)]
    menu_buttons = [get_circle(button_colors[0], 30), get_circle(button_colors[1], 30)]
    menu_index = 0

    while game.alive:
        mouse.update(Win_size, Default_size)

        # bliting text

        display.blit(title, [200, 100])
        if reason == "collapse":
            display.blit(reason_text, [350, 200])

        display.blit(circles, [80, 320])
        display.blit(points, [80, 420])

        display.blit(menu_buttons[menu_index], [770, 470])

        # event loop

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_f:
                    fs = not fs
                    if fs is False:
                        Win_size = Default_size
                        screenX = pygame.display.set_mode(Win_size)
                    else:
                        screenX = pygame.display.set_mode(monitor_size, pygame.FULLSCREEN)
                        d = pygame.display.get_surface()
                        Win_size = [int((d.get_height() / 2) * 3), d.get_height()]

                elif event.key == K_ESCAPE:
                    return screenX, fs, Win_size

            elif event.type == MOUSEBUTTONDOWN:
                if mouse.in_circle([800, 500], 30):
                    sounds["click"].play(0)
                    return screenX, fs, Win_size

            elif event.type == MOUSEMOTION:
                if mouse.in_circle([800, 500], 30):
                    menu_index = 1
                else:
                    menu_index = 0

        # basic loop config

        screenX.blit(pygame.transform.scale(display, Win_size), (0, 0))
        pygame.display.update()
        clock.tick(60)


menu(screen, False, Window_size)
# pip install pygame==2.0.0.dev16
