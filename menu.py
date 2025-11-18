from pico2d import *

class GameMenu:
    def __init__(self):
        self.menu_img = load_image('10.resource/menu.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = False

    def update(self):
        pass

    def draw(self):
        self.menu_img.draw(self.x, self.y)

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
