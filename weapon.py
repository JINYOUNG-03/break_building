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
        self.idle_offset_x, self.idle_offset_y = offset  # idle 상태 오프셋

        # idle 상태에서 작은 검 크기
        self.idle_w, self.idle_h = 24, 100

        # attack/defense 상태에서 큰 애니메이션 크기
        self.anim_w, self.anim_h = 300, 200  # y축을 줄여서 캐릭터 크기에 맞춤

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
        self.is_playing = True  # idle부터 시작
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
        # 위치 동기화: 상태에 따라 다른 위치 계산
        if self.state == 'idle':
            # idle 상태: 캐릭터 팔 위치에 작은 오프셋
            self.x = shared_state.x + self.idle_offset_x
            self.y = shared_state.y + self.idle_offset_y
        else:
            # attack/defense 상태: 캐릭터 중심 기준 (애니메이션 이미지가 중심에서 그려짐)
            self.x = shared_state.x + 50  # 캐릭터 중심에서 약간 오른쪽
            self.y = shared_state.y + 50  # 캐릭터 중심에서 약간 위

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

            # 상태에 따라 다른 크기로 그리기
            if self.state == 'idle':
                # idle: 작은 검 이미지
                img.draw(self.x, self.y, self.idle_w, self.idle_h)
            else:
                # attack/defense: 큰 애니메이션 이미지
                img.draw(self.x, self.y, self.anim_w, self.anim_h)
