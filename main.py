import sys

import pygame
import geocoder
from static_map import request_static_map
LAT_STEP = 0.008  # Шаги при движении карты по широте и долготе
LON_STEP = 0.002

class MapParams(object):
    """
    Параметры подгружаемой карты
    """
    def __init__(self):
        # Параметры по умолчанию.
        self.lon = '37.620070'
        self.lat = '55.753630'
        self.delta = None
        self.zoom = '7'
        self.type = "map"
        self.search_result = None  # Найденный объект для отображения на карте.
        self.use_postal_code = False

    def update(self, event):
        if event.key == pygame.K_LEFT:
            self.lon = str(float(self.lon) - LON_STEP * 2 ** (15 - float(self.zoom)))
        if event.key == pygame.K_UP:
            if int(self.zoom) < 23:
                self.zoom = str(int(self.zoom) + 1)
        if event.key == pygame.K_DOWN:
            if int(self.zoom) > 0:
                self.zoom = str(int(self.zoom) - 1)

    def search_toponym(self, address):
        code, toponym = geocoder.request_toponym(address)
        if code == 200:
            self.lon, self.lat = geocoder.get_coordinates(toponym)
            self.delta = geocoder.get_delta(toponym)


class App:
    """
    Класс отвечающий за запуск приложения. По умолчанию карта загружается на Москве
    """
    def __init__(self):
        pygame.init()
        self.width, self.height = 600, 480
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.fps = 50
        self.mp = MapParams()
        self.active = False
        self.text = 'Moscow'
        self.input_box = pygame.Rect(0, self.height - 30, self.height, 30)

    def terminate(self):
        pygame.quit()
        sys.exit()

    def load_image(self, mp):

        coords = mp.lon, mp.lat
        delta = mp.delta
        z = mp.zoom
        type = mp.type
        map_file = request_static_map(coords, delta, z, type)
        map = pygame.image.load(map_file)

        image = pygame.Surface(self.screen.get_size())
        image.fill(pygame.Color("lightblue"))
        font = pygame.font.Font(None, 35)
        text = font.render(self.text, True, (230, 255, 200))
        text_x = self.width - text.get_width()
        text_y = self.height - text.get_height()
        image.blit(text, (text_x, text_y))
        image.blit(map, (0, 0))
        pygame.draw.rect(image, pygame.Color("lightblue"), self.input_box)

        return image

    def run_app(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.terminate()
                if event.type == pygame.KEYUP:
                    self.mp.update(event)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_box.collidepoint(event.pos):
                        self.active = not self.active
                        self.text = ''
                    else:
                        self.active = False
                if event.type == pygame.KEYDOWN:
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            print(self.text)
                            self.mp.search_toponym(self.text)
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode

            self.screen.fill(pygame.Color('lightblue'))
            self.screen.blit(self.load_image(self.mp), (0, 0))

            pygame.display.flip()
            self.clock.tick(self.fps)


if __name__ == '__main__':
    app = App()
    app.run_app()
