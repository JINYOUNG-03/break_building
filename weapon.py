from pico2d import *
import shared_state
#아니 한 번 휘두르면 다시 원 상태가 아니고 오른쪽 왼쪽 반복해야함 자동차 와이퍼 생각
class Weapon:
    def __init__(self, owner=None, offset=(30, 0), image_path='10.resource/1. Basic.png'):
        self.weapon_img = load_image(image_path)
        self.owner = owner
        self.offset_x, self.offset_y = offset
        self.w, self.h = 24, 100   # 고정 출력 크기 100x24
        self.x, self.y = shared_state.x, shared_state.y
    def update(self, dt):
        # 항상 shared_state 값을 따라감 (owner가 있어도 owner는 shared_state를 업데이트함)
        self.x = shared_state.x + self.offset_x
        self.y = shared_state.y + self.offset_y

    def draw(self):
        self.weapon_img.draw(self.x, self.y, self.w, self.h)