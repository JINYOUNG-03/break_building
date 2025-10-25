from pico2d import *
from world import reset_world, update_world, render_world, handle_events
#해상도 540x960 설정

open_canvas(540, 960)
reset_world()

running = True

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
