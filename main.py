import os
import sys

import pygame
import pygame_gui as p_gui

from map import Map
from settings import HEIGHT, MANAGE_KEYS, VIEWS, WIDTH


def change_map_coords(key, map_obj):
    if key == pygame.K_PAGEUP:
        map_obj.reducing_spn()
    elif key == pygame.K_PAGEDOWN:
        map_obj.increasing_spn()
    elif key == pygame.K_RIGHT:
        map_obj.shifting_right()
    elif key == pygame.K_LEFT:
        map_obj.shifting_left()
    elif key == pygame.K_UP:
        map_obj.shifting_up()
    elif key == pygame.K_DOWN:
        map_obj.shifting_down()


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    manager = p_gui.UIManager((WIDTH, HEIGHT))
    change_view_button = p_gui.elements.UIButton(
        relative_rect=pygame.Rect(5, 5, 80, 30),
        text='View',
        manager=manager,
    )
    search_button = p_gui.elements.UIButton(
        relative_rect=pygame.Rect((5, 50), (80, 30)),
        text='Search',
        manager=manager,
    )
    entry_line = p_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((5, 85), (80, 30)),
        manager=manager,
    )
    reset_button = p_gui.elements.UIButton(
        relative_rect=pygame.Rect((5, 120), (80, 30)),
        text='Reset',
        manager=manager,
    )
    size_x, size_y = 20, 20
    coord_x, coord_y = 133.795384, -25.694768
    map_obj = Map(screen, coord_x, coord_y, size_x, size_y, VIEWS[0])
    map_obj.show_map()
    while True:
        time_delta = clock.tick(60) / 1000
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                os.remove("map.png")
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in MANAGE_KEYS:
                    change_map_coords(event.key, map_obj)
                    map_obj.show_map()
            if event.type == pygame.USEREVENT:
                if event.user_type == p_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == change_view_button:
                        map_obj.view = VIEWS[
                            (VIEWS.index(map_obj.view) + 1) % 3
                            ]
                    elif event.ui_element == search_button:
                        map_obj.search_object(entry_line.text)
                    elif event.ui_element == reset_button:
                        map_obj.reset_object()
                    map_obj.show_map()
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
