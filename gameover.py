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

        # 재시작 아이콘 로드
        self.restart_icon = load_image('10.resource/Button_06.png')  # Restart 아이콘

        # 버튼 영역 정의
        self.restart_button = {'x1': 170, 'y1': 200, 'x2': 370, 'y2': 280, 'text': 'RESTART', 'icon': self.restart_icon}

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

        # Restart 버튼 아이콘과 텍스트 표시
        btn = self.restart_button
        center_x = (btn['x1'] + btn['x2']) // 2
        center_y = (btn['y1'] + btn['y2']) // 2

        # 아이콘 이미지 그리기 (왼쪽에 배치)
        icon_size = 70
        icon_x = btn['x1'] + 50
        if 'icon' in btn and btn['icon']:
            btn['icon'].draw(icon_x, center_y, icon_size, icon_size)

        # 텍스트 (아이콘 오른쪽에 표시)
        text_x = icon_x + 50
        self.font.draw(text_x, center_y - 10, btn['text'], (255, 255, 255))

    def check_button_click(self, mouse_x, mouse_y):
        """
        마우스 클릭이 버튼 영역 안에 있는지 확인
        반환값: 'restart' 또는 None
        """
        btn = self.restart_button

        # 전체 버튼 영역 체크 (아이콘 + 텍스트 포함)
        if (btn['x1'] <= mouse_x <= btn['x2'] and
            btn['y1'] <= mouse_y <= btn['y2']):
            return 'restart'

        return None


