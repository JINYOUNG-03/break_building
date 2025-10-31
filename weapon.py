from pico2d import *
import shared_state

class Weapon:
    def __init__(self, owner=None, offset=(30, 0)):
        # 상태별 이미지 로드
        # idle: 기본 검 이미지 (정지)
        self.idle_img = [load_image('10.resource/1. Basic.png')]

        # attack: 공격 애니메이션 프레임들
        self.attack_img = [
            load_image('10.resource/attack_re_02.png'),
            load_image('10.resource/attack_re_03.png'),
            load_image('10.resource/attack_re_04.png'),
            load_image('10.resource/attack_re_05.png'),
            load_image('10.resource/attack_re_06.png'),
            load_image('10.resource/attack_re_07.png')
        ]

        self.defense_img = [load_image('10.resource/1. Basic.png')]

        self.owner = owner
        self.offset_x, self.offset_y = offset
        self.w, self.h = 24, 100   # 출력 크기
        self.x, self.y = shared_state.x, shared_state.y

        # 애니메이션 제어
        self.frame = 0
        self.anim_acc = 0.0
        self.anim_fps = 12.0
        self.frame_time = 1.0 / self.anim_fps

        # 상태 관리
        self.state = 'idle'  # 'idle', 'attack', 'defense'
        self.current_frames = self.idle_img
        self.total_frames = len(self.current_frames)

        # 애니메이션 재생 제어
        self.is_playing = False
        self.loop = True  # idle은 루프, attack/defense는 한 번만 재생

    def set_state(self, new_state):
        """상태 변경"""
        if self.state == new_state:
            return

        self.state = new_state
        self.frame = 0
        self.anim_acc = 0.0

        if new_state == 'idle':
            self.current_frames = self.idle_img
            self.is_playing = True
            self.loop = True
        elif new_state == 'attack':
            self.current_frames = self.attack_img
            self.is_playing = True
            self.loop = False
        elif new_state == 'defense':
            self.current_frames = self.defense_img
            self.is_playing = True
            self.loop = False

        self.total_frames = len(self.current_frames)

    def attack(self):
        """z키로 공격"""
        self.set_state('attack')

    def defend(self):
        """x키로 방어"""
        self.set_state('defense')

    def update(self, dt):
        # 위치 동기화
        self.x = shared_state.x + self.offset_x
        self.y = shared_state.y + self.offset_y

        # 애니메이션 재생 중일 때만 프레임 업데이트
        if self.is_playing and self.total_frames > 0:
            self.anim_acc += dt
            while self.anim_acc >= self.frame_time:
                self.frame += 1
                self.anim_acc -= self.frame_time

                # 프레임이 끝까지 갔을 때
                if self.frame >= self.total_frames:
                    if self.loop:
                        # idle은 반복
                        self.frame = 0
                    else:
                        # attack/defense는 끝나면 idle로 돌아감
                        self.frame = self.total_frames - 1
                        self.set_state('idle')

    def draw(self):
        if self.total_frames > 0:
            img = self.current_frames[self.frame]
            img.draw(self.x, self.y, self.w, self.h)
