from pico2d import *

#1080,1920 해상도을 하고 싶은데 노트북이 작아서 안보임 일단 /2로 줄여서 작업

class Start:
    def __init__(self):
        self.start_img = load_image('C:/3dp/break_building/10.resource/start_screen_main.png')
        self.x, self.y = 540/2, 960/2
        self.active =True
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
        self.menu_img = load_image('C:\3dp\break_building\10.resource/menu.png')
        self.x, self.y = 540/2, 960/2
        self.active = False

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




def update_world():
    for object in world:
        object.update()
    pass

def render_world():
    clear_canvas()
    for object in world:
        object.draw()
    update_canvas()

open_canvas(540,960)
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
                    world.clear()
                    current_screen = menu
                    world.append(current_screen)
    update_world()
    render_world()
    delay(0.05)

close_canvas()