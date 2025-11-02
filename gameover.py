from pico2d import *

class GameOver:
    def __init__(self):
        self.gameover_img = load_image('10.resource/EndBackground.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = False

    def update(self):
        pass

    def draw(self):
        self.gameover_img.draw(self.x, self.y)