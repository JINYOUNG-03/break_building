from pico2d import *
import random

class Missile:
    def __init__(self, x, y, speed=300.0):
        self.x = float(x)
        self.y = float(y)
        self.speed = float(speed)
        # 기본 크기
        self.w = 40
        self.h = 80

        # 애니메이션 프레임 로드 (missile1 ~ missile5)
        self.frames = []
        for i in range(1, 6):
            img = load_image(f'10.resource/missile{i}.png')
            self.frames.append(img)


        # 애니메이션 제어
        self.frame_index = 0
        self.anim_acc = 0.0
        self.anim_fps = 12.0  # 초당 프레임 수
        self.frame_time = 1.0 / self.anim_fps

    def update(self, dt=0.0):
        # 위치 업데이트
        if dt > 0:
            self.y -= self.speed * dt

        # 애니메이션 진행
        if self.has_frame_images and self.frame_time > 0:
            self.anim_acc += dt
            while self.anim_acc >= self.frame_time:
                self.frame_index = (self.frame_index + 1) % len(self.frames)
                self.anim_acc -= self.frame_time

    def draw(self):
        draw_x = int(round(self.x))
        draw_y = int(round(self.y))
        if self.has_frame_images:
            try:
                img = self.frames[self.frame_index]
                img.draw(draw_x, draw_y, self.w, self.h)
                return
            except Exception:
                # 프레임 그리기 실패하면 폴백으로 사각형 그리기
                pass

        # 이미지가 없거나 그리기 실패한 경우
        half_w = self.w / 2
        half_h = self.h / 2
        draw_rectangle(draw_x - half_w, draw_y - half_h, draw_x + half_w, draw_y + half_h)

    def get_bb(self):
        half_w = self.w / 2
        half_h = self.h / 2
        return (self.x - half_w, self.y - half_h,
                self.x + half_w, self.y + half_h)

    def is_offscreen(self, screen_bottom=0):
        return (self.y + self.h / 2) < screen_bottom


class MissileManager:
    def __init__(self, spawn_interval=6.0, spawn_x_min=60, spawn_x_max=480, spawn_y=950, speed=300.0):
        self.spawn_interval = spawn_interval
        self.spawn_timer = 0.0
        self.spawn_x_min = spawn_x_min
        self.spawn_x_max = spawn_x_max
        self.spawn_y = spawn_y
        self.speed = speed
        self.missiles = []

    def update(self, dt, active=False):
        # active일 때만 주기적으로 미사일 스폰
        if active:
            self.spawn_timer += dt
            while self.spawn_timer >= self.spawn_interval:
                x = random.uniform(self.spawn_x_min, self.spawn_x_max)
                m = Missile(x, self.spawn_y, self.speed)
                self.missiles.append(m)
                self.spawn_timer -= self.spawn_interval

        # 기존 미사일 업데이트
        for m in self.missiles:
            m.update(dt)

        # 화면 밖으로 나간 미사일 제거
        self.missiles = [m for m in self.missiles if not m.is_offscreen(0)]

    def draw(self):
        for m in self.missiles:
            m.draw()

    def clear(self):
        self.missiles.clear()
        self.spawn_timer = 0.0

    def remove(self, missile):
        try:
            self.missiles.remove(missile)
            return True
        except ValueError:
            return False
