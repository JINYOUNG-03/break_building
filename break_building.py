from pico2d import *
import random
#1080,1920 해상도을 하고 싶은데 노트북이 작아서 안보임 일단 /2로 줄여서 작업
open_canvas(540,960)
start_img = load_image('C:/3dp/break_building/10.resource/start_screen_main.png')
start_img.draw_now(270/2,480/2)

delay(5)

close_canvas()