import time
from pico2d import *
from world import reset_world, update_world, render_world, handle_events
#해상도 540x960 설정

open_canvas(540, 960)
reset_world()

prev_time = time.time()
running = True

while running:
    now = time.time()
    dt = now - prev_time
    prev_time = now

    handle_events()
    update_world(dt)
    render_world()
    delay(0.01)

close_canvas()
