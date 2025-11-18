from pico2d import *

class GameMenu:
    def __init__(self):
        self.menu_img = load_image('10.resource/menu.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = False
        self.font = load_font('ENCR10B.TTF', 30)

        # 버튼 영역 정의
        self.buttons = {
            'play': {'x1': 170, 'y1': 600, 'x2': 370, 'y2': 680, 'text': 'PLAY'},
            'tutorial': {'x1': 170, 'y1': 480, 'x2': 370, 'y2': 560, 'text': 'TUTORIAL'},
            'quit': {'x1': 170, 'y1': 360, 'x2': 370, 'y2': 440, 'text': 'QUIT'}
        }

    def update(self):
        pass

    def draw(self):
        self.menu_img.draw(self.x, self.y)

        # 버튼 영역 표시
        for button_name, btn in self.buttons.items():
            # 사각형 그리기 (빨간색 테두리)
            draw_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'])
            # 버튼 텍스트
            center_x = (btn['x1'] + btn['x2']) // 2
            center_y = (btn['y1'] + btn['y2']) // 2
            self.font.draw(center_x - 40, center_y - 10, btn['text'], (255, 255, 0))

    def check_button_click(self, mouse_x, mouse_y):
        """
        마우스 클릭이 버튼 영역 안에 있는지 확인
        반환값: 'play', 'tutorial', 'quit' 또는 None

        버튼 위치는 menu.png 이미지에 맞게 조정 필요
        """
        # Play 버튼 영역 (예시 좌표, 실제 이미지에 맞게 조정)
        if 170 <= mouse_x <= 370 and 600 <= mouse_y <= 680:
            return 'play'

        # Tutorial 버튼 영역 (예시 좌표)
        if 170 <= mouse_x <= 370 and 480 <= mouse_y <= 560:
            return 'tutorial'

        # Quit 버튼 영역 (예시 좌표)
        if 170 <= mouse_x <= 370 and 360 <= mouse_y <= 440:
            return 'quit'

        return None
