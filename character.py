from pico2d import *

class Character:
    def __init__(self):
        self.char_img = [load_image(f'10.resource/Char1_1_idle_{i+1}.png') for i in range(4)]
        self.x, self.y = 540 / 2, 140
        self.frame = 0
        self.scale = 2.0

        #애니메이션 델타 타임
        self.anim_fps=6.0
        self.frame_time=1.0/self.anim_fps
        self.time_acc = 0.0

    def set_scale(self, scale: float):
        self.scale = max(0.1, float(scale))

    def update(self,dt: float):
        #dt는 메인 루프에서 계산한 초 단위 델타 타임을 전달한다.
        self.time_acc +=dt
        while self.time_acc>=self.frame_time:
            self.frame = (self.frame + 1) % len(self.char_img)
            self.time_acc -= self.frame_time


    def draw(self):
        img = self.char_img[self.frame]
        w= int(img.w*self.scale)
        h= int(img.h*self.scale)
        img.draw(self.x, self.y, w, h)
