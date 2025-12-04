from pico2d import *

class WeaponSelect:
    def __init__(self):
        self.background = load_image('10.resource/Background_02.png')
        self.font = load_font('ENCR10B.TTF', 40)
        self.small_font = load_font('ENCR10B.TTF', 25)

        # 무기 데이터 (폴더 경로와 표시 이름)
        self.weapons = [
            # 첫 번째 줄
            {'name': 'Basic', 'folder': '3.animation/weapon animation/weapon', 'id': 'basic', 'icon_image': '10.resource/1. Basic.png'},
            {'name': 'Wooden', 'folder': '3.animation/weapon animation/weapon', 'id': 'wooden', 'icon_image': '10.resource/2. Wooden.png'},
            {'name': 'Ancient', 'folder': '3.animation/weapon animation/weapon', 'id': 'ancient', 'icon_image': '10.resource/3. Ancient.png'},
            {'name': 'Blood', 'folder': '3.animation/weapon animation/weapon', 'id': 'blood', 'icon_image': '10.resource/4. Blood.png'},
            # 두 번째 줄
            {'name': 'Chicken', 'folder': '3.animation/weapon animation/weapon', 'id': 'chicken', 'icon_image': '10.resource/5. Chicken.png'},
            {'name': 'Cutter', 'folder': '3.animation/weapon animation/weapon', 'id': 'cutter', 'icon_image': '10.resource/6. Cutter.png'},
            {'name': 'Green', 'folder': '3.animation/weapon animation/weapon', 'id': 'green', 'icon_image': '10.resource/7. Green.png'},
            {'name': 'Ice', 'folder': '3.animation/weapon animation/weapon', 'id': 'ice', 'icon_image': '10.resource/8. Ice.png'},
            # 세 번째 줄
            {'name': 'Lightning', 'folder': '3.animation/weapon animation/weapon', 'id': 'lightning', 'icon_image': '10.resource/10. Lightning.png'},
            {'name': 'Golden', 'folder': '3.animation/weapon animation/weapon', 'id': 'golden', 'icon_image': '10.resource/11. Golden.png'},
            {'name': 'Neptune', 'folder': '3.animation/weapon animation/weapon', 'id': 'neptune', 'icon_image': '10.resource/12. Neptune.png'},
            {'name': 'Night', 'folder': '3.animation/weapon animation/weapon', 'id': 'night', 'icon_image': '10.resource/13. Night.png'},
            # 네 번째 줄
            {'name': 'Pink', 'folder': '3.animation/weapon animation/weapon', 'id': 'pink', 'icon_image': '10.resource/14. Pink.png'},
            {'name': 'Rosen', 'folder': '3.animation/weapon animation/weapon', 'id': 'rosen', 'icon_image': '10.resource/15. Rosen.png'},
            {'name': 'Shark', 'folder': '3.animation/weapon animation/weapon', 'id': 'shark', 'icon_image': '10.resource/16. Shark.png'},
            {'name': 'Syringe', 'folder': '3.animation/weapon animation/weapon', 'id': 'syringe', 'icon_image': '10.resource/17. Syringe.png'},
        ]

        # 무기 아이콘 이미지 로드 (10.resource 폴더에서)
        for weapon in self.weapons:
            weapon['icon'] = None  # 기본값 설정
            try:
                weapon['icon'] = load_image(weapon['icon_image'])
            except Exception as e:
                print(f"Failed to load weapon icon: {weapon['icon_image']} - {e}")

        # 선택된 무기 인덱스
        self.selected_index = 0

        # 버튼 영역 설정 (4행 4열 그리드로 변경)
        self.button_width = 100
        self.button_height = 140
        self.grid_cols = 4  # 4열
        self.grid_rows = 4  # 4행
        self.start_x = 50
        self.start_y = 820  # 시작 위치를 더 위로
        self.spacing_x = 120  # 좁은 간격
        self.spacing_y = 170  # 행 간격

        # Back 버튼
        self.back_button = {
            'x1': 50, 'y1': 50, 'x2': 200, 'y2': 110,
            'text': 'BACK'
        }

        # Confirm 버튼
        self.confirm_button = {
            'x1': 340, 'y1': 50, 'x2': 490, 'y2': 110,
            'text': 'CONFIRM'
        }

    def get_weapon_button_rect(self, index):
        """무기 버튼의 영역 반환"""
        col = index % self.grid_cols
        row = index // self.grid_cols

        x = self.start_x + col * self.spacing_x
        y = self.start_y - row * self.spacing_y

        return {
            'x1': x,
            'y1': y - self.button_height,
            'x2': x + self.button_width,
            'y2': y
        }

    def update(self):
        pass

    def draw(self):
        # 배경
        self.background.draw(540 / 2, 960 / 2, 540, 960)

        # 제목
        self.font.draw(540 / 2 - 150, 900, 'SELECT WEAPON', (255, 255, 255))

        # 무기 버튼들
        for i, weapon in enumerate(self.weapons):
            rect = self.get_weapon_button_rect(i)
            center_x = (rect['x1'] + rect['x2']) // 2
            center_y = (rect['y1'] + rect['y2']) // 2

            # 선택된 무기는 테두리 표시
            if i == self.selected_index:
                draw_rectangle(rect['x1'] - 5, rect['y1'] - 5,
                             rect['x2'] + 5, rect['y2'] + 5)

            # 버튼 배경
            draw_rectangle(rect['x1'], rect['y1'], rect['x2'], rect['y2'])

            # 무기 아이콘
            if weapon['icon']:
                # 얇고 긴 칼 모양으로 표시 (폭 30, 높이 100)
                icon_width = 30
                icon_height = 100
                weapon['icon'].draw(center_x, center_y + 30, icon_width, icon_height)

            # 무기 이름
            text_width = len(weapon['name']) * 10
            self.small_font.draw(center_x - text_width // 2-15, center_y - 50,
                               weapon['name'], (255, 255, 255))

        # Back 버튼
        btn = self.back_button
        draw_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'])
        self.small_font.draw(btn['x1'] + 30, btn['y1'] + 25, btn['text'], (255, 255, 255))

        # Confirm 버튼
        btn = self.confirm_button
        draw_rectangle(btn['x1'], btn['y1'], btn['x2'], btn['y2'])
        self.small_font.draw(btn['x1'] + 15, btn['y1'] + 25, btn['text'], (255, 255, 255))

    def check_button_click(self, mouse_x, mouse_y):
        """
        마우스 클릭 처리
        반환값: ('back', None) 또는 ('confirm', weapon_id) 또는 ('weapon', index) 또는 (None, None)
        """
        # Back 버튼 체크
        btn = self.back_button
        if (btn['x1'] <= mouse_x <= btn['x2'] and
            btn['y1'] <= mouse_y <= btn['y2']):
            return ('back', None)

        # Confirm 버튼 체크
        btn = self.confirm_button
        if (btn['x1'] <= mouse_x <= btn['x2'] and
            btn['y1'] <= mouse_y <= btn['y2']):
            return ('confirm', self.weapons[self.selected_index]['id'])

        # 무기 버튼 체크
        for i, weapon in enumerate(self.weapons):
            rect = self.get_weapon_button_rect(i)
            if (rect['x1'] <= mouse_x <= rect['x2'] and
                rect['y1'] <= mouse_y <= rect['y2']):
                self.selected_index = i
                return ('weapon', i)

        return (None, None)

    def get_selected_weapon_id(self):
        """현재 선택된 무기 ID 반환"""
        return self.weapons[self.selected_index]['id']
