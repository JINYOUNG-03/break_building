from pico2d import *

class GameMenu:
    def __init__(self):
        self.menu_img = load_image('10.resource/menu.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = False
        self.font = load_font('ENCR10B.TTF', 30)

        # 버튼 아이콘 이미지 로드
        # 사용자 제공 이미지: play_button.png, tutorial_button.png, quit_button.png
        # 이미지 파일이 없으면 기존 리소스 사용
        try:
            self.play_icon = load_image('10.resource/play_button.png')  # 파란 재생 버튼
        except:
            self.play_icon = load_image('10.resource/Button_06.png')

        try:
            self.tutorial_icon = load_image('10.resource/tutorial_button.png')  # 톱니바퀴
        except:
            self.tutorial_icon = load_image('10.resource/Button_07.png')

        try:
            self.quit_icon = load_image('10.resource/quit_button.png')  # X 아이콘
        except:
            self.quit_icon = load_image('10.resource/Button_09.png')

        # 버튼 영역 정의
        self.buttons = {
            'play': {'x1': 170, 'y1': 600, 'x2': 370, 'y2': 680, 'text': 'PLAY', 'icon': self.play_icon},
            'tutorial': {'x1': 170, 'y1': 480, 'x2': 370, 'y2': 560, 'text': 'TUTORIAL', 'icon': self.tutorial_icon},
            'quit': {'x1': 170, 'y1': 360, 'x2': 370, 'y2': 440, 'text': 'QUIT', 'icon': self.quit_icon}
        }

    def update(self):
        pass

    def draw(self):
        self.menu_img.draw(self.x, self.y)

        # 버튼 아이콘만 표시 (테두리 없이)
        for button_name, btn in self.buttons.items():
            # 버튼 중앙 좌표
            center_x = (btn['x1'] + btn['x2']) // 2
            center_y = (btn['y1'] + btn['y2']) // 2

            # 아이콘 이미지 그리기 (크게 표시)
            icon_size = 80
            if 'icon' in btn and btn['icon']:
                btn['icon'].draw(center_x, center_y, icon_size, icon_size)

    def check_button_click(self, mouse_x, mouse_y):
        """
        마우스 클릭이 버튼 이미지 영역 안에 있는지 확인
        반환값: 'play', 'tutorial', 'quit' 또는 None
        """
        icon_size = 80

        for button_name, btn in self.buttons.items():
            center_x = (btn['x1'] + btn['x2']) // 2
            center_y = (btn['y1'] + btn['y2']) // 2

            # 이미지 영역 체크 (원형으로 가정)
            if (center_x - icon_size//2 <= mouse_x <= center_x + icon_size//2 and
                center_y - icon_size//2 <= mouse_y <= center_y + icon_size//2):
                return button_name

        return None
