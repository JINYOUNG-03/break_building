from pico2d import *

class Building:
    def __init__(self, x, y, fall_speed=200.0):
        self.x = float(x)
        self.y = float(y)
        self.fall_speed = float(fall_speed)
        self.falling = False
        self.w = 540
        self.h = 50
        self.image = load_image('10.resource/building_1.png')


    def start_fall(self):
        self.falling = True

    def stop(self):
        self.falling = False

    def update(self, dt=0.0):
        if self.falling and dt > 0:
            self.y -= self.fall_speed * dt

    def draw(self):
        draw_x = int(round(self.x))
        draw_y = int(round(self.y))

        # 이미지 그리기
        if self.image:
            self.image.draw(draw_x, draw_y, self.w, self.h)
        else:
            # 이미지 없을 때 빨간 사각형으로 표시
            hw = self.w / 2
            hh = self.h / 2
            draw_rectangle(draw_x - hw, draw_y - hh, draw_x + hw, draw_y + hh)

        # 바운딩 박스 그리기 (디버그용)
        x1, y1, x2, y2 = self.get_bb()
        draw_rectangle(x1, y1, x2, y2)
    def is_offscreen(self, screen_bottom=0):
        return (self.y + self.h / 2) < screen_bottom

    def get_bb(self):
        half_w = self.w / 2
        half_h = self.h / 2
        return self.x - half_w, self.y - half_h + 15, self.x + half_w, self.y + half_h


class BuildingManager:
    def __init__(self, spawn_interval=1.0, spawn_x=270, spawn_y=1000, fall_speed=200.0, screen_bottom=0, min_gap=5):
        self.spawn_interval = spawn_interval
        self.spawn_timer = 0.0
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.fall_speed = fall_speed
        self.screen_bottom = screen_bottom
        self.buildings = []
        self.min_gap = min_gap  # 건물 간 최소 간격 (픽셀)

        # 난이도 증가 관련
        self.difficulty_timer = 0.0
        self.difficulty_interval = 3.0  # 3초마다 난이도 증가
        self.initial_spawn_interval = spawn_interval
        self.initial_fall_speed = fall_speed
        self.min_spawn_interval = 0.5  # 최소 스폰 간격
        self.max_fall_speed = 500.0  # 최대 낙하 속도

    def _can_spawn(self, new_building):
        """새 건물이 기존 건물들과 겹치지 않는지 확인"""
        new_bb = new_building.get_bb()
        x1_new, y1_new, x2_new, y2_new = new_bb

        for existing in self.buildings:
            ex_bb = existing.get_bb()
            x1_ex, y1_ex, x2_ex, y2_ex = ex_bb

            # Y축 겹침 검사 (min_gap 고려)
            if not (y2_new + self.min_gap < y1_ex or y1_new - self.min_gap > y2_ex):
                # Y축이 겹치면 스폰 불가
                return False
        return True

    def _increase_difficulty(self):
        """난이도 증가: 스폰 간격 감소, 낙하 속도 증가"""
        # 스폰 간격을 10% 감소 (최소값 제한)
        self.spawn_interval = max(self.min_spawn_interval, self.spawn_interval * 0.9)

        # 낙하 속도를 10% 증가 (최대값 제한)
        self.fall_speed = min(self.max_fall_speed, self.fall_speed * 1.1)

        # 기존 건물들의 낙하 속도도 업데이트
        for building in self.buildings:
            building.fall_speed = self.fall_speed

    def update(self, dt, gamestart_active):
        # gamestart 상태일 때만 주기적으로 스폰
        if gamestart_active:
            # 난이도 증가 타이머
            self.difficulty_timer += dt
            if self.difficulty_timer >= self.difficulty_interval:
                self._increase_difficulty()
                self.difficulty_timer = 0.0

            self.spawn_timer += dt
            while self.spawn_timer >= self.spawn_interval:
                b = Building(self.spawn_x, self.spawn_y, self.fall_speed)
                # 겹치지 않을 때만 스폰
                if self._can_spawn(b):
                    b.start_fall()
                    self.buildings.append(b)
                self.spawn_timer -= self.spawn_interval

        # 기존 빌딩 업데이트
        for b in self.buildings:
            b.update(dt)

        # 화면 밖으로 나간 빌딩 제거
        self.buildings = [b for b in self.buildings if not b.is_offscreen(self.screen_bottom)]
        #여기를 나중에 빌딩 제거가 아니라 게임 오버 화면 나오게 해야함.

    def draw(self):
        for b in self.buildings:
            b.draw()

    def start_all(self):
        for b in self.buildings:
            b.start_fall()

    def manual_spawn(self):
        """수동으로 빌딩 하나를 즉시 생성하고 떨어뜨림"""
        b = Building(self.spawn_x, self.spawn_y, self.fall_speed)
        if self._can_spawn(b):
            b.start_fall()
            self.buildings.append(b)

    def clear(self):
        self.buildings.clear()
        self.spawn_timer = 0.0
        self.difficulty_timer = 0.0  # 난이도 타이머도 리셋
        self.spawn_interval = self.initial_spawn_interval  # 초기값으로 복원
        self.fall_speed = self.initial_fall_speed  # 초기값으로 복원

    def destroy_building(self, building):
        """지정된 단일 빌딩을 리스트에서 제거
        - 빌딩이 없으면 False 반환, 제거되면 True 반환.
        """
        try:
            self.buildings.remove(building)
            return True
        except ValueError:
            return False

def draw_rectangle(x1, y1, x2, y2):
    """사각형을 그리는 함수"""
    draw_line(x1, y1, x2, y1)  # 아래쪽 선
    draw_line(x2, y1, x2, y2)  # 오른쪽 선
    draw_line(x2, y2, x1, y2)  # 위쪽 선
