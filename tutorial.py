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

        # 홈 아이콘 로드
        self.back_icon = load_image('10.resource/Button_07.png')  # Back to menu

        self.attack_img = load_image('10.resource/attack_sword_04.png')

        # 버튼 영역 정의 (x, y, width, height)
        self.back_button = {
            'x': 270,
            'y': 150,
            'width': 200,
            'height': 80,
            'text': 'BACK',
            'icon': self.back_icon
        }

    def draw(self):
        self.tuto_img.draw(self.x, self.y)
        # 제목
        self.title_font.draw(120, 850, 'HOW TO PLAY', (255, 255, 255))

        self.attack_img.draw(450,730,200,100)
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

        # Back 버튼 아이콘과 텍스트 표시
        btn = self.back_button

        # 아이콘 이미지 그리기 (왼쪽에 배치)
        icon_size = 70
        icon_x = btn['x'] - 50
        if 'icon' in btn and btn['icon']:
            btn['icon'].draw(icon_x, btn['y'], icon_size, icon_size)

        # 텍스트 (아이콘 오른쪽에 표시)
        text_x = icon_x + 50
        self.font.draw(text_x, btn['y'] - 10, btn['text'], (255, 255, 255))

        update_canvas()

    def update(self):
        pass

    def check_button_click(self, mouse_x, mouse_y):
        """
        마우스 클릭이 버튼 영역 안에 있는지 확인
        반환값: 'back' 또는 None
        """
        btn = self.back_button

        # 전체 버튼 영역 체크 (아이콘 + 텍스트 포함)
        x1 = btn['x'] - btn['width']//2
        y1 = btn['y'] - btn['height']//2
        x2 = btn['x'] + btn['width']//2
        y2 = btn['y'] + btn['height']//2

        if (x1 <= mouse_x <= x2 and y1 <= mouse_y <= y2):
            return 'back'
        return None

