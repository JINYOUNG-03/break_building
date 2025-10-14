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
    global running
    running = True

    global world
    world = []

    global start
    start = Start()
    world.append(start)

    global screen
    screen = start
    world.append(screen)

    global menu
    menu = GameMenu()
    world.append(menu)

    global current_screen
    current_screen = start

    global character
    character = Character()
    world.append(character)

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
            else:
                if current_screen == start:
                    current_screen = menu
                    world.append(current_screen)
                if current_screen == menu:
                    if event.key == SDLK_s:
                        world.clear()
                        current_screen = start
                        world.append(current_screen)

    update_world()
    render_world()
    delay(0.05)

close_canvas()
