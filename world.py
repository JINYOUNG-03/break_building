from start import Start
from menu import GameMenu
from gamestart import GameStart
from character import Character

def reset_world():
    global running, start, menu, gamestart, character, current_screen, world
    running = True
    start = Start()
    menu = GameMenu()
    gamestart = GameStart()
    character = Character()
    current_screen = start
    world = [current_screen]
from pico2d import *
def update_world(dt):
    for obj in world:
        try:
            obj.update(dt)
        except TypeError:
            obj.update()

def render_world():
    clear_canvas()
    for obj in world:
        obj.draw()
    update_canvas()

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

def handle_events():
    global running, current_screen, world
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif current_screen == start and event.key == SDLK_m:
                current_screen = menu
                world = [current_screen]
            elif current_screen == menu and event.key == SDLK_s:
                current_screen = gamestart
                world = [current_screen, character]
            elif current_screen == gamestart and event.key == SDLK_r:
                current_screen = start
                world = [current_screen]
