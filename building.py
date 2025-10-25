from pico2d import *
import random

class Building:
    def __init__(self, x, y, fall_speed=200.0):
        self.x = float(x)
        self.y = float(y)
        self.fall_speed = float(fall_speed)
        self.falling = False
        self.w = 540
        self.h = 50
        self.image = load_image('10.resource/building_1.png')


    def start_fall(self):
        self.falling = True

    def stop(self):
        self.falling = False

    def update(self, dt=0.0):
        if self.falling and dt > 0:
            self.y -= self.fall_speed * dt

    def draw(self):
        draw_x = int(round(self.x))
        draw_y = int(round(self.y))
        if self.image:
            self.image.draw(draw_x, draw_y, self.w, self.h)
        else:
            # 이미지 없을 때 빨간 사각형으로 표시
            hw = self.w / 2
            hh = self.h / 2
            from pico2d import draw_rectangle
            draw_rectangle(draw_x - hw, draw_y - hh, draw_x + hw, draw_y + hh)

    def is_offscreen(self, screen_bottom=0):
        return (self.y + self.h / 2) < screen_bottom


class BuildingManager:
    def __init__(self, spawn_interval=1.0, spawn_x=270, spawn_y=1000, fall_speed=200.0, screen_bottom=0):
        self.spawn_interval = spawn_interval
        self.spawn_timer = 0.0
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.fall_speed = fall_speed
        self.screen_bottom = screen_bottom
        self.buildings = []

    def update(self, dt, gamestart_active):
        # gamestart 상태일 때만 주기적으로 스폰
        if gamestart_active:
            self.spawn_timer += dt
            while self.spawn_timer >= self.spawn_interval:
                b = Building(self.spawn_x, self.spawn_y, self.fall_speed)
                b.start_fall()
                self.buildings.append(b)
                self.spawn_timer -= self.spawn_interval

        # 기존 빌딩 업데이트
        for b in self.buildings:
            b.update(dt)

        # 화면 밖으로 나간 빌딩 제거
        self.buildings = [b for b in self.buildings if not b.is_offscreen(self.screen_bottom)]

    def draw(self):
        for b in self.buildings:
            b.draw()

    def start_all(self):
        for b in self.buildings:
            b.start_fall()

    def manual_spawn(self):
        """수동으로 빌딩 하나를 즉시 생성하고 떨어뜨림"""
        b = Building(self.spawn_x, self.spawn_y, self.fall_speed)
        b.start_fall()
        self.buildings.append(b)

    def clear(self):
        self.buildings.clear()
        self.spawn_timer = 0.0
