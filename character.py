from pico2d import *
import shared_state

width= 45
height=80
class Character:
    def __init__(self):
        self.char_img = [load_image(f'10.resource/Char1_1_idle_{i+1}.png') for i in range(4)]
        self.jump_img = [load_image(f'10.resource/Char1_1_jump_{i+1}.png') for i in range(3)]
        self.x, self.y = 540 / 2, 140
        self.frame = 0
        self.scale = 2.0

        # 애니메이션 제어
        self.anim_fps = 6.0
        self.frame_time = 1.0 / self.anim_fps
        self.anim_acc = 0.0      # idle 누적 시간
        self.jump_acc = 0.0      # jump 누적 시간

        # 지정된 x값을 이동 (540 기준)
        self.positions = [540 * 0.25, 540 * 0.5, 540 * 0.75]
        self.pos_index = 1
        self.target_x = self.positions[self.pos_index]

        self.move_speed = 400.0

        self.is_jumping = False
        self.jump_frame = 0
        self.ground_y = 140
        self.velocity_y = 0.0
        self.jump_power = 800.0
        self.gravity = 1600.0

    def set_scale(self, scale: float):
        self.scale = max(0.1, float(scale))

    def set_positions(self, positions):
        if positions and len(positions) >= 1:
            self.positions = positions
            self.pos_index = max(0, min(self.pos_index, len(self.positions) - 1))
            self.target_x = self.positions[self.pos_index]

    def move_left(self):
        if self.pos_index > 0:
            self.pos_index -= 1
            self.target_x = self.positions[self.pos_index]

    def move_right(self):
        if self.pos_index < len(self.positions) - 1:
            self.pos_index += 1
            self.target_x = self.positions[self.pos_index]

    def jump(self):
        if not self.is_jumping and self.y == self.ground_y:
            self.is_jumping = True
            self.velocity_y = self.jump_power
            self.jump_frame = 0
            self.jump_acc = 0.0

    def update(self, dt: float):
        # 좌우 이동
        shared_state.set_pos(self.x-width, self.y + height/2)
        if self.x != self.target_x:
            direction = 1 if self.target_x > self.x else -1
            step = self.move_speed * dt
            remaining = abs(self.target_x - self.x)
            if step >= remaining:
                self.x = self.target_x
            else:
                self.x += direction * step

        # 점프 중
        if self.is_jumping:
            self.jump_acc += dt
            while self.jump_acc >= self.frame_time:
                self.jump_frame = (self.jump_frame + 1) % len(self.jump_img)
                self.jump_acc -= self.frame_time

            self.velocity_y -= self.gravity * dt
            self.y += self.velocity_y * dt

            if self.y <= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.velocity_y = 0.0
                self.jump_frame = 0
                self.jump_acc = 0.0
                self.anim_acc = 0.0
        else:
            # 대기 애니메이션
            self.anim_acc += dt
            while self.anim_acc >= self.frame_time:
                self.frame = (self.frame + 1) % len(self.char_img)
                self.anim_acc -= self.frame_time

    def draw(self):
        if self.is_jumping:
            img = self.jump_img[self.jump_frame]
        else:
            img = self.char_img[self.frame]
        w = int(img.w * self.scale)
        h = int(img.h * self.scale)
        img.draw(self.x, self.y, w, h)
