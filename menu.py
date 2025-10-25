from pico2d import *

class GameMenu:
    def __init__(self):
        self.menu_img = load_image('10.resource/menu.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = False

    def update(self):
        pass

    def draw(self):
        self.menu_img.draw(self.x, self.y)
