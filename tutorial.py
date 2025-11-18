"""
조작 키 안내 화면 (Tutorial Screen)
"""
from pico2d import *

class Tutorial:
    def __init__(self):
        self.tuto_img = load_image('10.resource/tutorial.png')

        self.x, self.y = 540 / 2, 960 / 2

        self.font = load_font('ENCR10B.TTF', 30)
        self.title_font = load_font('ENCR10B.TTF', 50)


        # 버튼 영역 정의 (x, y, width, height)
        self.back_button = {
            'x': 270,
            'y': 150,
            'width': 200,
            'height': 80,
            'text': 'BACK'
        }

    def draw(self):
        self.tuto_img.draw(self.x, self.y)
        # 제목
        self.title_font.draw(120, 850, 'HOW TO PLAY', (255, 255, 255))

        # 조작 키 안내
        instructions = [
            ('Z Key', 'Attack', 700),
            ('X Key', 'Defense', 600),
            ('Left/A Key', 'Move Left', 500),
            ('Right/D Key', 'Move Right', 400),
        ]

        for key, action, y in instructions:
            self.font.draw(100, y, f'{key}:', (255, 200, 0))
            self.font.draw(300, y, action, (255, 255, 255))

        # Back 버튼 영역 표시
        btn = self.back_button
        draw_rectangle(
            btn['x'] - btn['width']//2,
            btn['y'] - btn['height']//2,
            btn['x'] + btn['width']//2,
            btn['y'] + btn['height']//2
        )
        self.font.draw(btn['x'] - 40, btn['y'] - 10, btn['text'], (255, 255, 0))

        update_canvas()

    def update(self):
        pass

    def check_button_click(self, mouse_x, mouse_y):
        """
        마우스 클릭이 버튼 영역 안에 있는지 확인
        반환값: 'back' 또는 None
        """
        btn = self.back_button
        if (btn['x'] - btn['width']//2 <= mouse_x <= btn['x'] + btn['width']//2 and
            btn['y'] - btn['height']//2 <= mouse_y <= btn['y'] + btn['height']//2):
            return 'back'
        return None

