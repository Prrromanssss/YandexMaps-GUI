import os
import sys

import pygame
import pygame_gui

import settings


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


def controls(manager, map, widgets):
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            os.remove('map.png')
            sys.exit()
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == widgets['find']:
                    coords = map.search_object(widgets['entry'].text)
                    if coords:
                        map.coord_x, map.coord_y = coords
                elif event.ui_element == widgets['reset']:
                    map.reset()
                    widgets['entry'].set_text('')
                    widgets['address'].set_text('')
                elif event.ui_element == widgets['postal_code_in']:
                    map.change_postal_code_on(widgets['postal_code_in'])
                map.show_address(widgets['address'])
            elif event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == widgets['address']:
                    widgets['address'].set_text(map.address)
            elif event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                map.set_l(event.text)
        elif event.type == pygame.KEYDOWN:
            if event.key in settings.MANAGE_KEYS:
                change_map_coords(event.key, map)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_coords = event.pos
            if event.button == 1 and 40 < mouse_coords[1] < 410:
                coords = map.get_coord_from_mouse_coord(mouse_coords)
                map.search_object(widgets['entry'].text, coords)
                map.show_address(widgets['address'])
            elif event.button == 3 and 40 < mouse_coords[1] < 410:
                coords = map.get_coord_from_mouse_coord(mouse_coords)
                map.search_organization(widgets['entry'].text, coords)
                map.show_address(widgets['address'])
        manager.process_events(event)


def create_widgets(manager):
    pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
        options_list=['схема', 'спутник', 'гибрид'],
        starting_option='схема',
        relative_rect=pygame.Rect((515, 0), (85, 40)),
        manager=manager,
    )
    find = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((100, 0), (100, 40)),
        text='Найти',
        manager=manager,
    )
    entry = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((0, 0), (100, 40)),
        manager=manager,
    )
    reset = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((230, 0), (250, 40)),
        text='Сброс поискового результата',
        manager=manager,
    )
    address = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((0, 410), (300, 40)),
        manager=manager,
    )
    postal_code_in = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((310, 410), (230, 40)),
        text='Добавить почтовый индекс',
        manager=manager,
    )
    widgets = {
        'entry': entry,
        'find': find,
        'reset': reset,
        'address': address,
        'postal_code_in': postal_code_in
    }
    return widgets
