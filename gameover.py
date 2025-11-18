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

        self.font = load_font('ENCR10B.TTF', 30)

        # 버튼 영역 정의
        self.restart_button = {'x1': 170, 'y1': 200, 'x2': 370, 'y2': 280, 'text': 'RESTART'}

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

        # Restart 버튼 영역 표시
        btn = self.restart_button
        draw_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'])
        center_x = (btn['x1'] + btn['x2']) // 2
        center_y = (btn['y1'] + btn['y2']) // 2
        self.font.draw(center_x - 50, center_y - 10, btn['text'], (255, 255, 0))

    def check_button_click(self, mouse_x, mouse_y):
        """
        마우스 클릭이 버튼 영역 안에 있는지 확인
        반환값: 'restart' 또는 None

        버튼 위치는 EndBackground.png 이미지에 맞게 조정 필요
        """
        # Restart 버튼 영역 (예시 좌표, 실제 이미지에 맞게 조정)
        if 170 <= mouse_x <= 370 and 200 <= mouse_y <= 280:
            return 'restart'

        return None


