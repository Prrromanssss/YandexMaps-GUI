import pygame
import pygame_gui

import settings
from core import controls, create_widgets
from map import Map


def main():
    screen = pygame.display.set_mode(settings.SIZE)
    manager = pygame_gui.UIManager(settings.SIZE)
    clock = pygame.time.Clock()
    x, y = 20, 20
    coord_x, coord_y = 133.795384, -25.694768
    map = Map(screen, coord_x, coord_y, x, y)
    widgets = create_widgets(manager)
    while True:
        map.show_map()
        time_delta = clock.tick(60) / 1000
        controls(manager, map, widgets)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
