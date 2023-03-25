import sys

import pygame
import requests

import settings


class Map:
    def __init__(self, screen, coord_x, coord_y, x, y):
        self.screen = screen
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.x = x
        self.y = y
        self.duration = 1
        self.map_params = {}
        self.address = ''
        self.postal_code = None
        self.postal_code_on = False

    def reset(self):
        self.address = ''
        self.postal_code = None
        if self.map_params.get('pt'):
            self.map_params.pop('pt')

    def show_address(self, address_widget):
        address = self.address
        if self.postal_code_on and self.postal_code:
            address += f', {self.postal_code}'
        address_widget.set_text(address)

    def set_postal_code(self):
        search_api_server = settings.GEOCODE_MAP_URL
        search_params = {
            'apikey': settings.APIKEY,
            'geocode': self.address,
            'format': 'json',
        }
        response = requests.get(search_api_server, params=search_params)
        if not response:
            return
        json_response = response.json()
        try:
            toponym = (
                json_response['response']['GeoObjectCollection']
                ['featureMember'][0]['GeoObject']['metaDataProperty']
                ['GeocoderMetaData']
            )
            toponym_address = (
                toponym['AddressDetails']['Country']
                ['AdministrativeArea']['Locality']
            )
            postal_code = (
                toponym_address['Thoroughfare']['Premise']
                ['PostalCode']['PostalCodeNumber']
            )
        except KeyError:
            postal_code = None
        self.postal_code = postal_code

    def search_object(self, text, coords=None):
        if not coords:
            coords = (self.coord_x, self.coord_y)
        data = self.get_geocoords_by_text(text, coords)
        if not data:
            if self.map_params.get('pt'):
                self.map_params.pop('pt')
            self.reset()
            return
        coords, self.address = data
        self.set_postal_code()
        self.set_pt(coords)
        return coords

    def search_organization(self, text, coords=None):
        if not coords:
            coords = (self.coord_x, self.coord_y)
        data = self.get_orgcoords_by_text(text, coords)
        if not data:
            if self.map_params.get('pt'):
                self.map_params.pop('pt')
            self.reset()
            return
        coords, self.address = data
        self.set_postal_code()
        self.set_pt(coords)
        return coords

    def get_orgcoords_by_text(self, text, coords):
        search_api_server = settings.SEARCH_MAP_URL
        search_params = {
            'apikey': settings.GEOCODE_APIKEY,
            'text': text,
            'll': f'{coords[0]},{coords[1]}',
            'lang': 'ru_RU',
            'type': 'biz',
            'results': 1,
        }
        response = requests.get(search_api_server, params=search_params)
        if not response:
            return
        json_response = response.json()
        if not json_response['features']:
            return
        organization = json_response['features'][0]
        point = organization['geometry']['coordinates']
        address = organization['properties']['CompanyMetaData']['address']
        radius = 0.05
        if (
            (point[0] - coords[0]) ** 2 +
            (point[1] - coords[1]) ** 2 > radius ** 2
        ):
            return
        return point, address

    def set_pt(self, coords):
        coord_x, coord_y = coords
        self.map_params['pt'] = f'{coord_x},{coord_y},pm2rdl'

    def set_l(self, text):
        dct_l = settings.VIEWS
        self.map_params['l'] = dct_l[text]

    def get_geocoords_by_text(self, text, coords):
        search_api_server = settings.SEARCH_MAP_URL
        search_params = {
            'apikey': settings.GEOCODE_APIKEY,
            'text': text,
            'll': f'{coords[0]},{coords[1]}',
            'lang': 'ru_RU',
            'type': 'geo',
            'results': 1,
        }
        response = requests.get(search_api_server, params=search_params)
        if not response:
            return
        json_response = response.json()
        if not json_response['features']:
            return
        organization = json_response['features'][0]
        point = organization['geometry']['coordinates']
        address = organization['properties']['GeocoderMetaData']['text']
        return point, address

    def show_map(self):
        map_file = 'map.png'
        map_api_server = settings.STATIC_MAP_URL
        map_params = {
            'll': f'{self.coord_x},{self.coord_y}',
            'spn': f'{self.x},{self.y}',
            'l': 'map',
            'apikey': settings.APIKEY
        }
        for key, value in self.map_params.items():
            map_params[key] = value
        response = requests.get(map_api_server, params=map_params)
        if not response:
            print('Ошибка выполнения запроса:')
            print(
                'Http статус:',
                response.status_code,
                '(',
                response.reason,
                ')'
            )
            sys.exit(1)
        with open(map_file, 'wb') as file:
            file.write(response.content)
        self.screen.blit(pygame.image.load(map_file), (0, 0))

    def reducing_spn(self):
        self.x /= 1.5
        self.y /= 1.5

    def increasing_spn(self):
        x, y = self.x, self.y
        x *= 1.5
        if x > 90:
            x = 90
        y *= 1.5
        if y > 90:
            y = 90
        self.x, self.y = x, y

    def shifting_right(self):
        coord_x = self.coord_x
        coord_x += self.x * 2.
        self.coord_x = -(-coord_x % 180) if coord_x >= 180 else coord_x

    def shifting_left(self):
        coord_x = self.coord_x
        coord_x -= self.x * 2.
        self.coord_x = coord_x % 180 if coord_x <= -180 else coord_x

    def shifting_up(self):
        coord_y = self.coord_y
        coord_y += self.y * 2. * self.duration
        if abs(coord_y) >= 90:
            self.coord_y = -(-coord_y % 90) if coord_y < 0 else -coord_y % 90
            self.coord_x = -self.coord_x
            self.duration = -self.duration
        else:
            self.coord_y = coord_y

    def shifting_down(self):
        coord_y = self.coord_y
        coord_y -= self.y * 2. * self.duration
        if abs(coord_y) >= 90:
            self.coord_y = -(-coord_y % 90) if coord_y < 0 else -coord_y % 90
            self.coord_x = -self.coord_x
            self.duration = -self.duration
        else:
            self.coord_y = coord_y

    def change_postal_code_on(self, postal_code_on_widget):
        if self.postal_code_on:
            self.postal_code_on = False
            postal_code_on_widget.set_text('Добавить почтовый индекс')
        else:
            self.postal_code_on = True
            postal_code_on_widget.set_text('Убрать почтовый индекс')

    def get_coord_from_mouse_coord(self, mouse_coords):
        x, y = settings.SIZE
        mouse_coord_x, mouse_coord_y = mouse_coords
        if self.coord_x > 0:
            coord_x = round(
                (self.coord_x - self.x) + mouse_coord_x * ((2 * self.x) / x), 6
            )
        else:
            coord_x = round(
                (self.coord_x + self.x) - mouse_coord_x * ((2 * self.x) / x), 6
            )
        if self.coord_y > 0:
            coord_y = round(
                (self.coord_y - self.y) + mouse_coord_y * ((2 * self.y) / y), 6
            )
        else:
            coord_y = round(
                (self.coord_y + self.y) - mouse_coord_y * ((2 * self.y) / y), 6
            )
        return coord_x, coord_y
