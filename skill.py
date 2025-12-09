from pico2d import *
import time

class Skill:
    def __init__(self):
        # HeavyAttack 애니메이션 로드
        self.heavy_attack_frames = [
            load_image('10.resource/HeavyAttack_01.png'),
            load_image('10.resource/HeavyAttack_02.png'),
            load_image('10.resource/HeavyAttack_03.png'),
            load_image('10.resource/HeavyAttack_04.png'),
            load_image('10.resource/HeavyAttack_05.png'),
            load_image('10.resource/HeavyAttack_06.png'),
            load_image('10.resource/HeavyAttack_07.png'),
            load_image('10.resource/HeavyAttack_08.png'),
        ]

        # TailShot 이미지 로드
        self.tailshot_img = load_image('10.resource/TailShot.png')

        # 스킬 상태
        self.is_active = False
        self.animation_time = 0.0
        self.animation_frame = 0
        self.animation_fps = 30.0  # 더 빠른 애니메이션 (20 -> 30)
        self.animation_frame_time = 1.0 / self.animation_fps

        # TailShot 상태
        self.tailshot_active = False
        self.tailshot_y = 0
        self.tailshot_x = 0
        self.tailshot_speed = 1200.0  # 더 빠르게 상승 (800 -> 1200)

        # 쿨타임
        self.cooldown = 10.0  # 10초
        self.last_used_time = -100.0  # 처음에는 사용 가능하도록

        # 캐릭터 위치
        self.char_x = 0
        self.char_y = 0

    def can_use(self):
        """스킬 사용 가능한지 확인"""
        current_time = time.time()
        return (current_time - self.last_used_time) >= self.cooldown

    def get_remaining_cooldown(self):
        """남은 쿨타임 반환"""
        current_time = time.time()
        elapsed = current_time - self.last_used_time
        remaining = max(0, self.cooldown - elapsed)
        return remaining

    def activate(self, char_x, char_y):
        """스킬 활성화"""
        if not self.can_use():
            return False

        self.is_active = True
        self.animation_time = 0.0
        self.animation_frame = 0
        self.char_x = char_x
        self.char_y = char_y
        self.last_used_time = time.time()

        # TailShot은 애니메이션 후에 활성화됨
        self.tailshot_active = False

        return True

    def update(self, dt):
        """스킬 업데이트"""
        if not self.is_active:
            return

        # HeavyAttack 애니메이션 업데이트
        if self.animation_frame < len(self.heavy_attack_frames):
            self.animation_time += dt
            while self.animation_time >= self.animation_frame_time:
                self.animation_frame += 1
                self.animation_time -= self.animation_frame_time

                # 애니메이션이 끝나면 TailShot 발사
                if self.animation_frame >= len(self.heavy_attack_frames):
                    self.tailshot_active = True
                    self.tailshot_x = self.char_x
                    self.tailshot_y = self.char_y
                    break

        # TailShot 상승 업데이트
        if self.tailshot_active:
            self.tailshot_y += self.tailshot_speed * dt

            # 화면 상단을 넘어가면 스킬 종료
            if self.tailshot_y > 960:
                self.is_active = False
                self.tailshot_active = False

    def draw(self):
        """스킬 그리기"""
        if not self.is_active:
            return

        # HeavyAttack 애니메이션 그리기
        if self.animation_frame < len(self.heavy_attack_frames):
            img = self.heavy_attack_frames[self.animation_frame]
            img.draw(self.char_x, self.char_y, img.w * 1.5, img.h * 1.5)

        # TailShot 그리기
        if self.tailshot_active:
            self.tailshot_img.draw(self.tailshot_x, self.tailshot_y,
                                   self.tailshot_img.w * 0.8, self.tailshot_img.h * 0.8)

    def get_tailshot_bb(self):
        """TailShot 바운딩 박스 반환"""
        if not self.tailshot_active:
            return None

        w = self.tailshot_img.w * 0.8 / 2
        h = self.tailshot_img.h * 0.8 / 2

        return (self.tailshot_x - w, self.tailshot_y - h,
                self.tailshot_x + w, self.tailshot_y + h)

