from pico2d import *

#540,960해상도

class Start:
    def __init__(self):
        self.start_img = load_image('10.resource/start_screen_main.png')
        self.x, self.y = 540/2, 960/2
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

class GameMenu:
    def __init__(self):
        self.menu_img = load_image('10.resource/menu.png')
        self.x, self.y = 540/2, 960/2
        self.active = False
    def update(self):
        pass
    def draw(self):
        self.menu_img.draw(self.x, self.y)

class GameStart:
    def __init__(self):
        self.gamestart_img = load_image('10.resource/Background_02.png')
        self.x, self.y = 540/2, 960/2
        self.active = False
    def update(self):
        pass
    def draw(self):
        self.gamestart_img.draw(self.x, self.y)

class Character:
    def __init__(self):
        self.char_img = [load_image(f'10.resource/Char1_1_idle_{i+1}.png') for i in range(4)]
        self.x, self.y = 540/2, 120 #270에 120이 딱 바닥임
        self.frame = 0
    def update(self):
        self.frame = (self.frame + 1) % 4 #프레임이 4개라서 0~3
        pass
    def draw(self):
        self.char_img[self.frame].draw(self.x, self.y)

def reset_world():
    global running, start, menu, gamestart, character, current_screen, world
    running = True
    start = Start()
    menu = GameMenu()
    gamestart = GameStart()
    character = Character()
    current_screen = start
    world = [current_screen]

def update_world():
    for object in world:
        object.update()
    pass

def render_world():
    clear_canvas()
    for object in world:
        object.draw()
    update_canvas()

open_canvas(540, 960)
reset_world()

while running:
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
                world = [current_screen,character]
            elif current_screen == gamestart and event.key == SDLK_r:
                current_screen = start
                world = [current_screen]

    update_world()
    render_world()
    delay(0.01)

close_canvas()
