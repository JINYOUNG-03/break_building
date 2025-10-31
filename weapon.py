from pico2d import *
import shared_state

class Weapon:
    def __init__(self, owner=None, offset=(30, 0)):
        # 상태별 이미지 로드
        # idle: 기본 검 이미지 (정지)
        self.idle_img = [load_image('10.resource/1. Basic.png')]

        # attack: 공격 애니메이션 프레임들
        self.attack_left_to_right = [
            load_image('10.resource/attack_re_02.png'),
            load_image('10.resource/attack_re_03.png'),
            load_image('10.resource/attack_re_04.png'),
        ]

        self.attack_right_to_left = [
            load_image('10.resource/attack_re_07.png'),
            load_image('10.resource/attack_re_08.png'),
            load_image('10.resource/attack_re_09.png')
        ]

        self.defense_img = [load_image('10.resource/1. Basic.png')]

        self.owner = owner
        self.idle_offset_x, self.idle_offset_y = offset  # idle 상태 오프셋

        # idle 상태에서 작은 검 크기
        self.idle_w, self.idle_h = 24, 100

        # attack/defense 상태에서 큰 애니메이션 크기
        # 원본 비율 550x330을 유지하면서 적당한 크기로 스케일링
        self.anim_w, self.anim_h = 330, 198  # 550:330 비율 유지 (0.6배)

        self.x, self.y = shared_state.x, shared_state.y

        # 애니메이션 제어
        self.frame = 0
        self.anim_acc = 0.0
        self.anim_fps = 30.0
        self.frame_time = 1.0 / self.anim_fps

        # 상태 관리
        self.state = 'idle'  # 'idle', 'attack', 'defense'
        self.current_frames = self.idle_img
        self.total_frames = len(self.current_frames)

        # 애니메이션 재생 제어
        self.is_playing = True  # idle부터 시작
        self.loop = True  # idle은 루프, attack/defense는 한 번만 재생

        # 공격 방향 관리 (와이퍼처럼 번갈아가며)
        self.attack_direction = 'left_to_right'  # 'left_to_right' 또는 'right_to_left'

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
            # 항상 left_to_right 이미지 사용 (right_to_left는 draw에서 반전)
            self.current_frames = self.attack_left_to_right
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
        # owner(캐릭터)의 상태를 따라감
        if self.owner and hasattr(self.owner, 'state'):
            # 캐릭터의 공격 방향 먼저 동기화
            if hasattr(self.owner, 'attack_direction'):
                self.attack_direction = self.owner.attack_direction

            if self.owner.state != self.state:
                self.set_state(self.owner.state)

            # 위치 동기화: owner의 실제 좌표 사용
            owner_x = self.owner.x
            owner_y = self.owner.y

            self.x = owner_x - 15
            self.y = owner_y + 30

            # 공격 상태일 때 캐릭터 프레임과 완벽하게 동기화
            if self.state == 'attack' and hasattr(self.owner, 'action_frame'):
                # 캐릭터의 현재 방향에 따라 사용할 이미지 결정
                if self.attack_direction == 'left_to_right':
                    char_attack_img = self.owner.attack_left_to_right
                else:
                    char_attack_img = self.owner.attack_right_to_left

                # 캐릭터의 프레임 진행도 계산 (0~1 사이)
                char_total_frames = len(char_attack_img)
                char_progress = self.owner.action_frame / char_total_frames

                # 무기 프레임을 캐릭터 진행도에 맞춰 설정
                self.frame = int(char_progress * self.total_frames)
                if self.frame >= self.total_frames:
                    self.frame = self.total_frames - 1

        # 애니메이션 재생 (attack 상태가 아닐 때만 자동 진행)
        if self.is_playing and self.total_frames > 0 and self.state != 'attack':
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
                # 오른쪽→왼쪽 공격 시 좌우 반전
                if self.state == 'attack' and self.attack_direction == 'right_to_left':
                    img.composite_draw(0, 'h', self.x, self.y, self.anim_w, self.anim_h)
                else:
                    img.draw(self.x, self.y, self.anim_w, self.anim_h)
