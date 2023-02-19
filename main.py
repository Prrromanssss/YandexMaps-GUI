import os
import sys

import pygame
import pygame_gui as p_gui
import requests

from settings import HEIGHT, VIEWS, WIDTH


def get_map(coord_x, coord_y, size_x, size_y, view):
    map_request = (
        f"https://static-maps.yandex.ru/1.x/"
        f"?ll={coord_x},{coord_y}&spn={size_x},{size_y}&l={view}"
        )
    return map_request


def show_map(screen, coord_x, coord_y, size_x, size_y, view):
    map_file = "map.png"
    response = requests.get(get_map(coord_x, coord_y, size_x, size_y, view))
    if not response:
        print("Ошибка выполнения запроса:")
        print(get_map(coord_x, coord_y, size_x, size_y))
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (80, 0))


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    manager = p_gui.UIManager((WIDTH, HEIGHT))
    change_view_button = p_gui.elements.UIButton(
        relative_rect=pygame.Rect(5, 5, 70, 30),
        text='View',
        manager=manager,
    )
    size_x, size_y = 20, 20
    coord_x, coord_y = 133.795384, -25.694768
    duration = 1
    view = VIEWS[0]
    show_map(screen, coord_x, coord_y, size_x, size_y, view)

    while True:
        time_delta = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os.remove("map.png")
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    size_x /= 1.5
                    size_y /= 1.5
                if event.key == pygame.K_PAGEDOWN:
                    size_x *= 1.5
                    if size_x > 90:
                        size_x = 90
                    size_y *= 1.5
                    if size_y > 90:
                        size_y = 90
                if event.key == pygame.K_RIGHT:
                    coord_x += size_x * 2.
                    coord_x = -(-coord_x % 180) if coord_x >= 180 else coord_x
                if event.key == pygame.K_LEFT:
                    coord_x -= size_x * 2.
                    coord_x = coord_x % 180 if coord_x <= -180 else coord_x
                if event.key == pygame.K_UP:
                    coord_y += size_y * 2. * duration
                    if abs(coord_y) >= 90:
                        coord_y = (
                            -(-coord_y % 90) if coord_y < 0
                            else -coord_y % 90
                            )
                        coord_x = -coord_x
                        duration = -duration
                if event.key == pygame.K_DOWN:
                    coord_y -= size_y * 2. * duration
                    if abs(coord_y) >= 90:
                        coord_y = (
                            -(-coord_y % 90) if coord_y < 0
                            else -coord_y % 90
                            )
                        coord_x = -coord_x
                        duration = -duration
                show_map(screen, coord_x, coord_y, size_x, size_y, view)
            if event.type == pygame.USEREVENT:
                if event.user_type == p_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == change_view_button:
                        view = VIEWS[(VIEWS.index(view) + 1) % 3]
                show_map(screen, coord_x, coord_y, size_x, size_y, view)
            manager.process_events(event)
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
