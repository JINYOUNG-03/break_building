from pico2d import *

#1080,1920 해상도을 하고 싶은데 노트북이 작아서 안보임 일단 /2로 줄여서 작업

class Start:
    def __init__(self):
        self.start_img = load_image('C:/3dp/break_building/10.resource/start_screen_main.png')
        self.x, self.y = 270, 480
        self.active =True
    def update(self):
        pass
    def draw(self):
        if self.active:
            self.start_img.draw(self.x, self.y)
    def handle_event(self, event):
        if event.type == SDL_MOUSEBUTTONDOWN:
            self.active = False
            return True
        return False


def reset_world():
    global running
    running = True

    global world
    world = []

    global start
    start = Start()
    world.append(start)


open_canvas(540,960)

reset_world()

def update_world():
    for object in world:
        object.update()
    pass

def render_world():
    clear_canvas()
    for object in world:
        object.draw()
    update_canvas()

while running:
    update_world()
    render_world()
    delay(0.05)

close_canvas()