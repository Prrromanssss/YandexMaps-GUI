import sys

import pygame
import requests

import settings


class Map:
    def __init__(self, screen, coord_x, coord_y, size_x, size_y, view):
        self.screen = screen
        self.coord_x, self.coord_y = coord_x, coord_y
        self.size_x, self.size_y = size_x, size_y
        self.view = view
        self.duration = 1
        self.map_params = {}

    def get_map(self):
        params = {
            "ll": f'{self.coord_x},{self.coord_y}',
            "spn": f'{self.size_x},{self.size_y}',
            "l": self.view,
            "apikey": settings.APIKEY,
            }
        for key, value in self.map_params.items():
            params[key] = value
        return settings.STATIC_MAP_URL, params

    def show_map(self):
        map_file = "map.png"
        map_request, map_params = self.get_map()
        response = requests.get(map_request, map_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(self.get_map())
            print(f"Http статус: {response.status_code} ( {response.reason} )")
            sys.exit(1)

        with open(map_file, "wb") as file:
            file.write(response.content)

        self.screen.blit(pygame.image.load(map_file), (90, 0))

    def reducing_spn(self):
        self.size_x /= 1.5
        self.size_y /= 1.5

    def increasing_spn(self):
        size_x, size_y = self.size_x, self.size_y
        size_x *= 1.5
        if size_x > 90:
            size_x = 90
        size_y *= 1.5
        if size_y > 90:
            size_y = 90
        self.size_x, self.size_y = size_x, size_y

    def shifting_right(self):
        coord_x = self.coord_x
        coord_x += self.size_x * 2.
        self.coord_x = -(-coord_x % 180) if coord_x >= 180 else coord_x

    def shifting_left(self):
        coord_x = self.coord_x
        coord_x -= self.size_x * 2.
        self.coord_x = coord_x % 180 if coord_x <= -180 else coord_x

    def shifting_up(self):
        coord_y = self.coord_y
        coord_y += self.size_y * 2. * self.duration
        if abs(coord_y) >= 90:
            self.coord_y = -(-coord_y % 90) if coord_y < 0 else -coord_y % 90
            self.coord_x = -self.coord_x
            self.duration = -self.duration
        else:
            self.coord_y = coord_y

    def shifting_down(self):
        coord_y = self.coord_y
        coord_y -= self.size_y * 2. * self.duration
        if abs(coord_y) >= 90:
            self.coord_y = -(-coord_y % 90) if coord_y < 0 else -coord_y % 90
            self.coord_x = -self.coord_x
            self.duration = -self.duration
        else:
            self.coord_y = coord_y

    def set_pt(self, coords):
        coord_x, coord_y = coords
        self.map_params["pt"] = f"{coord_x},{coord_y},pm2rdl"

    def search_object(self, text):
        coords = (self.coord_x, self.coord_y)
        data = self.get_geocoords_by_text(text, coords)
        if not data:
            if self.map_params.get("pt"):
                self.map_params.pop("pt")
            return
        coords, address = data
        self.set_pt(coords)
        self.coord_x, self.coord_y = coords

    def reset_object(self):
        self.map_params["pt"] = ""

    @staticmethod
    def get_geocoords_by_text(text, coords):
        search_params = {
            "apikey": settings.GEOCODE_APIKEY,
            "text": text,
            "ll": f'{coords[0]},{coords[1]}',
            "lang": "ru_RU",
            "type": 'geo',
            "results": 1,
        }
        response = requests.get(settings.SEARCH_MAP_URL, params=search_params)
        if not response:
            return
        json_response = response.json()
        if not json_response["features"]:
            return
        organization = json_response["features"][0]
        point = organization["geometry"]["coordinates"]
        address = organization["properties"]["GeocoderMetaData"]["text"]
        return point, address
