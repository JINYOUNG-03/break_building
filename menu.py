from pico2d import *

class GameMenu:
    def __init__(self):
        self.menu_img = load_image('10.resource/menu.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = False
        self.font = load_font('ENCR10B.TTF', 30)

        # 버튼 아이콘 이미지 로드
        self.play_icon = load_image('10.resource/Direction_13.png')  # Game Start
        self.tutorial_icon = load_image('10.resource/Button_11.png')  # Tutorial
        self.quit_icon = load_image('10.resource/Button_09.png')  # Quit

        # 버튼 영역 정의
        self.buttons = {
            'play': {'x1': 170, 'y1': 600, 'x2': 370, 'y2': 680, 'text': 'GAME START', 'icon': self.play_icon},
            'tutorial': {'x1': 170, 'y1': 480, 'x2': 370, 'y2': 560, 'text': 'TUTORIAL', 'icon': self.tutorial_icon},
            'quit': {'x1': 170, 'y1': 360, 'x2': 370, 'y2': 440, 'text': 'QUIT', 'icon': self.quit_icon}
        }

    def update(self):
        pass

    def draw(self):
        self.menu_img.draw(self.x, self.y)

        # 버튼 아이콘과 텍스트 표시
        for button_name, btn in self.buttons.items():
            # 버튼 중앙 좌표
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
        반환값: 'play', 'tutorial', 'quit' 또는 None
        """
        for button_name, btn in self.buttons.items():
            # 전체 버튼 영역 체크 (아이콘 + 텍스트 포함)
            if (btn['x1'] <= mouse_x <= btn['x2'] and
                btn['y1'] <= mouse_y <= btn['y2']):
                return button_name

        return None
