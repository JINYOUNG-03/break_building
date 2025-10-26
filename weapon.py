from pico2d import *
#아니 한 번 휘두르면 다시 원 상태가 아니고 오른쪽 왼쪽 반복해야함 자동차 와이퍼 생각
class Weapon:
    def __init__(self):
        self.weapon_img = load_image(f'10.resource/1. Basic.png')
        self.x, self.y = 254,175
        self.w, self.h = 24,100

    def update(self,dt):
        pass

    def draw(self):
        self.weapon_img.draw(self.x, self.y,self.w, self.h)
