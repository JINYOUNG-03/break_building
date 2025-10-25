import time
from pico2d import *
import world

# 해상도 540x960 설정
open_canvas(540, 960)
world.reset_world()

prev_time = time.time()

while world.running:
    now = time.time()
    dt = now - prev_time
    prev_time = now

    world.handle_events()
    world.update_world(dt)
    world.render_world()
    delay(0.01)

close_canvas()
