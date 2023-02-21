import os

import pygame
from dotenv import load_dotenv

load_dotenv()

SIZE = WIDTH, HEIGHT = 600, 450

VIEWS = ('map', 'sat', 'sat,skl')

MANAGE_KEYS = (
    pygame.K_PAGEDOWN,
    pygame.K_PAGEUP,
    pygame.K_RIGHT,
    pygame.K_LEFT,
    pygame.K_UP,
    pygame.K_DOWN,
    )

STATIC_MAP_URL = "https://static-maps.yandex.ru/1.x/"

SEARCH_MAP_URL = "https://search-maps.yandex.ru/v1/"

APIKEY = os.environ.get('APIKEY', 'summy-dummy-key')

GEOCODE_APIKEY = os.environ.get('GEOCODE_APIKEY', 'summy-dummy-key')
