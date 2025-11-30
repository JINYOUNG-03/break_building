"""
건물 파괴 시 떨어지는 파편 효과
"""
from pico2d import *
import random


class Fragment:
    """건물 파편 클래스"""
    def __init__(self, x, y, fragment_img):
        self.x = x
        self.y = y
        self.img = fragment_img

        # 랜덤한 속도와 방향
        self.vx = random.uniform(-100, 100)  # 좌우 속도
        self.vy = random.uniform(100, 300)   # 위쪽 초기 속도
        self.gravity = -800.0  # 중력

        # 회전
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-360, 360)

        # 크기
        self.scale = random.uniform(0.1, 0.3)

        # 수명
        self.lifetime = 1.0  # 1초 후 사라짐
        self.alpha = 1.0

    def update(self, dt):
        """파편 업데이트"""
        # 물리 업데이트
        self.vy += self.gravity * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

        # 회전
        self.rotation += self.rotation_speed * dt

        # 수명 감소
        self.lifetime -= dt

        # 페이드 아웃 (마지막 0.3초)
        if self.lifetime < 0.3:
            self.alpha = self.lifetime / 0.3

        # 바닥에 닿으면 속도 감소 (바운스 효과)
        if self.y < 140:
            self.y = 140
            self.vy = -self.vy * 0.3  # 반발 계수
            self.vx *= 0.7  # 마찰
            self.rotation_speed *= 0.7

    def is_dead(self):
        """파편이 사라져야 하는지 확인"""
        return self.lifetime <= 0

    def draw(self):
        """파편 그리기"""
        if self.img and self.alpha > 0:
            # 회전과 크기를 적용하여 그리기
            self.img.rotate_draw(
                math.radians(self.rotation),
                self.x, self.y,
                self.img.w * self.scale,
                self.img.h * self.scale
            )


class FragmentManager:
    """파편 관리자"""
    def __init__(self):
        self.fragments = []
        # 파편 이미지 로드
        self.fragment_images = [
            load_image('10.resource/fragment_1.png'),
            load_image('10.resource/fragment_2.png'),
            load_image('10.resource/fragment_3.png')
        ]

    def create_fragments(self, x, y, count=5):
        """
        특정 위치에서 파편 생성
        x, y: 건물 파괴 위치
        count: 생성할 파편 개수
        """
        for _ in range(count):
            # 랜덤한 이미지 선택
            img = random.choice(self.fragment_images)
            # 건물 위치 주변에서 랜덤하게 생성
            offset_x = random.uniform(-30, 30)
            offset_y = random.uniform(-30, 30)
            fragment = Fragment(x + offset_x, y + offset_y, img)
            self.fragments.append(fragment)

    def update(self, dt):
        """모든 파편 업데이트"""
        for fragment in self.fragments:
            fragment.update(dt)

        # 수명이 다한 파편 제거
        self.fragments = [f for f in self.fragments if not f.is_dead()]

    def draw(self):
        """모든 파편 그리기"""
        for fragment in self.fragments:
            fragment.draw()

    def clear(self):
        """모든 파편 제거"""
        self.fragments.clear()

