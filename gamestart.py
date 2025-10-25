from pico2d import *

class GameStart:
    def __init__(self):
        self.gamestart_img = load_image('10.resource/Background_02.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = False

    def update(self):
        pass

    def draw(self):
        self.gamestart_img.draw(self.x, self.y)
