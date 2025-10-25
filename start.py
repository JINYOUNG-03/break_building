from pico2d import *

class Start:
    def __init__(self):
        self.start_img = load_image('10.resource/start_screen_main.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = True

    def update(self):
        pass

    def draw(self):
        if self.active:
            self.start_img.draw(self.x, self.y)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            self.active = False
            return True
        return False
