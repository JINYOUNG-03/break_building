from pico2d import *

class Character:
    def __init__(self):
        self.char_img = [load_image(f'10.resource/Char1_1_idle_{i+1}.png') for i in range(4)]
        self.x, self.y = 540 / 2, 140
        self.frame = 0
        self.scale = 2.0

    def set_scale(self, scale: float):
        self.scale = max(0.1, float(scale))

    def update(self):
        self.frame = (self.frame + 1) % 4

    def draw(self):
        img = self.char_img[self.frame]
        w= int(img.w*self.scale)
        h= int(img.h*self.scale)
        img.draw(self.x, self.y, w, h)
