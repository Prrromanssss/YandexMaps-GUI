import os
import sys

import pygame
import requests


def get_map(coord_x, coord_y, x, y):
    map_request = (
        f"https://static-maps.yandex.ru/1.x/"
        f"?ll={coord_x},{coord_y}&spn={x},{y}&l=sat"
        )
    return map_request


def show_map(screen, coord_x, coord_y,x, y):
    map_file = "map.png"
    response = requests.get(get_map(coord_x, coord_y,x, y))
    if not response:
        print("Ошибка выполнения запроса:")
        print(get_map(133.795384, -25.694768, 20, 20))
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))


def main():
    screen = pygame.display.set_mode((600, 450))
    x, y = 20, 20
    coord_x, coord_y = 133.795384, -25.694768
    show_map(screen, coord_x, coord_y, x, y)
    duration = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                os.remove("map.png")
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    x /= 1.5
                    y /= 1.5
                if event.key == pygame.K_PAGEDOWN:
                    x *= 1.5
                    if x > 90:
                        x = 90
                    y *= 1.5
                    if y > 90:
                        y = 90
                if event.key == pygame.K_RIGHT:
                    coord_x += x * 2.
                    coord_x = -(-coord_x % 180) if coord_x >= 180 else coord_x
                if event.key == pygame.K_LEFT:
                    coord_x -= x * 2.
                    coord_x = coord_x % 180 if coord_x <= -180 else coord_x
                if event.key == pygame.K_UP:
                    coord_y += y * 2. * duration
                    if abs(coord_y) >= 90:
                        coord_y = -(-coord_y % 90) if coord_y < 0 else -coord_y % 90
                        coord_x = -coord_x
                        duration = -duration
                if event.key == pygame.K_DOWN:
                    coord_y -= y * 2. * duration
                    if abs(coord_y) >= 90:
                        coord_y = -(-coord_y % 90) if coord_y < 0 else -coord_y % 90
                        coord_x = -coord_x
                        duration = -duration
                show_map(screen, coord_x, coord_y, x, y)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
