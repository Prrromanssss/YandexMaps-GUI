import os
import sys

import pygame
import requests


def get_map(x, y):
    map_request = (
        f"https://static-maps.yandex.ru/1.x/"
        f"?ll=133.795384%2C-25.694768&spn={x},{y}&l=sat"
        )
    return map_request


def show_map(screen, x, y):
    map_file = "map.png"
    response = requests.get(get_map(x, y))
    if not response:
        print("Ошибка выполнения запроса:")
        print(get_map(20, 20))
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))


def main():
    screen = pygame.display.set_mode((600, 450))
    x, y = 20, 20
    show_map(screen, x, y)
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
                    show_map(screen, x, y)
                if event.key == pygame.K_PAGEDOWN:
                    x *= 1.5
                    if x > 90:
                        x = 90
                    y *= 1.5
                    if y > 90:
                        y = 90
                    show_map(screen, x, y)
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    main()
