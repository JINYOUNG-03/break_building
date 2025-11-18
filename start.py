from pico2d import *

class Start:
    def __init__(self):
        self.start_img = load_image('10.resource/start_screen_main.png')
        self.x, self.y = 540 / 2, 960 / 2
        self.active = True

    def update(self):
        pass

    def draw(self):
        if self.active:
            self.start_img.draw(self.x, self.y)

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            self.active = False
            return True
        return False

    def check_button_click(self, mouse_x, mouse_y):
        """
        마우스 클릭 시 화면 전체를 클릭 영역으로 처리
        반환값: 'start' 또는 None
        """
        # 화면 어디든 클릭하면 시작
        if 0 <= mouse_x <= 540 and 0 <= mouse_y <= 960:
            return 'start'
        return None
