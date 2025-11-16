from pico2d import *

class GameOver:
    def __init__(self):
        self.gameover_img = load_image('10.resource/EndBackground.png')
        # defeat 이미지 로드
        self.defeat_img = load_image('10.resource/Char1_1_defeat1.png')

        self.x, self.y = 540 / 2, 960 / 2
        self.active = False

        # defeat 이미지 표시 위치 (215~315 사이의 중앙 x, y=892)
        self.defeat_center_x = (215 + 315) / 2
        self.defeat_center_y = 920
        # 원하는 폭
        self.defeat_width = 100

    def update(self):
        pass

    def draw(self):
        # 배경 먼저 그리기
        self.gameover_img.draw(self.x, self.y)

        # defeat 이미지의 종횡비에 맞춰 높이 계산 후 그리기
        if self.defeat_img:
            w = self.defeat_width
            h = int(self.defeat_img.h * (w / self.defeat_img.w))
            self.defeat_img.draw(self.defeat_center_x, self.defeat_center_y, w, h)


