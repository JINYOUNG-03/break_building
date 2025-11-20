from pico2d import *
import shared_state

width= 45
height=80
class Character:
    def __init__(self):
        self.char_img = [load_image(f'10.resource/Char1_1_idle_{i+1}.png') for i in range(4)]
        self.defense_img = [load_image('10.resource/Char1_1_def.png')]

        self.x, self.y = 540 / 2, 140
        self.frame = 0
        self.scale = 2.0

        # 애니메이션 제어
        self.anim_fps = 6.0
        self.frame_time = 1.0 / self.anim_fps
        self.anim_acc = 0.0      # idle 누적 시간

        # 지정된 x값을 이동 (540 기준)
        self.positions = [540 * 0.25, 540 * 0.5, 540 * 0.75]
        self.pos_index = 1
        self.target_x = self.positions[self.pos_index]

        self.move_speed = 400.0

        # 상태 관리 ('idle', 'attack', 'defense')
        self.state = 'idle'
        self.action_frame = 0  # attack/defense 프레임
        self.action_acc = 0.0
        self.action_fps = 20.0  # attack/defense 애니메이션 속도
        self.action_frame_time = 1.0 / self.action_fps

        # 공격 방향 관리 (와이퍼처럼 번갈아가며)
        self.attack_direction = 'left_to_right'

        self.attack_left_to_right = [
            load_image('10.resource/Char1_1_attack_01.png'),
            load_image('10.resource/Char1_1_attack_02.png'),
            load_image('10.resource/Char1_1_attack_04.png'),
        ]

        self.attack_right_to_left = [
            load_image('10.resource/Char1_1_attack_04.png'),
            load_image('10.resource/Char1_1_attack_03.png'),
            load_image('10.resource/Char1_1_attack_01.png')
        ]

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

    def attack(self):
        """공격 상태로 전환"""
        if self.state not in ['attack', 'defense']:
            self.state = 'attack'
            self.action_frame = 0
            self.action_acc = 0.0

    def defend(self):
        """방어 상태로 전환"""
        if self.state not in ['attack', 'defense']:
            self.state = 'defense'
            self.action_frame = 0
            self.action_acc = 0.0

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

        if self.state == 'attack':
            # 현재 방향에 따라 사용할 이미지 결정
            current_attack_img = self.attack_left_to_right if self.attack_direction == 'left_to_right' else self.attack_right_to_left

            # 공격 애니메이션
            self.action_acc += dt
            while self.action_acc >= self.action_frame_time:
                self.action_frame += 1
                self.action_acc -= self.action_frame_time
                if self.action_frame >= len(current_attack_img):
                    # 공격 방향 전환 (와이퍼처럼)
                    if self.attack_direction == 'left_to_right':
                        self.attack_direction = 'right_to_left'
                    else:
                        self.attack_direction = 'left_to_right'

                    # 공격 애니메이션 끝나면 idle로
                    self.state = 'idle'
                    self.action_frame = 0
                    self.action_acc = 0.0
                    self.anim_acc = 0.0
                    break
        elif self.state == 'defense':
            # 방어 애니메이션
            self.action_acc += dt
            if self.action_acc >= 0.5:  # 0.5초 후 idle로
                self.state = 'idle'
                self.action_frame = 0
                self.action_acc = 0.0
                self.anim_acc = 0.0
        else:
            # idle 애니메이션
            self.anim_acc += dt
            while self.anim_acc >= self.frame_time:
                self.frame = (self.frame + 1) % len(self.char_img)
                self.anim_acc -= self.frame_time

    def draw(self):
        if self.state == 'attack':
            # 방향에 따라 다른 이미지 리스트 사용
            if self.attack_direction == 'left_to_right':
                img = self.attack_left_to_right[self.action_frame]
            else:
                img = self.attack_right_to_left[self.action_frame]
        elif self.state == 'defense':
            img = self.defense_img[0]
        else:  # idle
            img = self.char_img[self.frame]

        w = int(img.w * self.scale)
        h = int(img.h * self.scale)
        img.draw(self.x, self.y, w, h)

        # 바운딩 박스 그리기 (디버그용)
        x1, y1, x2, y2 = self.get_bb()
        draw_rectangle(x1, y1, x2, y2)

    def get_bb(self):
        """바운딩 박스 반환 (x1, y1, x2, y2)"""
        # 캐릭터 이미지 크기 계산
        if self.state == 'attack':
            if self.attack_direction == 'left_to_right':
                img = self.attack_left_to_right[self.action_frame]
            else:
                img = self.attack_right_to_left[self.action_frame]
        elif self.state == 'defense':
            img = self.defense_img[0]
        else:
            img = self.char_img[self.frame]

        w = int(img.w * self.scale)
        h = int(img.h * self.scale)
        half_w = w / 2
        half_h = h / 2

        return (self.x - half_w, self.y - half_h,
                self.x + half_w, self.y + half_h - 10)
