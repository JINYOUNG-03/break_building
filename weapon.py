from pico2d import *
import shared_state



class Weapon:
    # 무기 타입별 이미지 파일 정의
    WEAPON_DATA = {
        'basic': {'idle': '1. Basic.png', 'name': 'Basic', 'folder': '1. Basic'},
        'wooden': {'idle': '2. Wooden.png', 'name': 'Wooden', 'folder': '2. Wooden'},
        'ancient': {'idle': '3. Ancient.png', 'name': 'Ancient', 'folder': '3. Ancient'},
        'blood': {'idle': '4. Blood.png', 'name': 'Blood', 'folder': '4. Blood'},
        'chicken': {'idle': '5. Chicken.png', 'name': 'Chicken', 'folder': '5. Chicken'},
        'cutter': {'idle': '6. Cutter.png', 'name': 'Cutter', 'folder': '6. Cutter'},
        'green': {'idle': '7. Green.png', 'name': 'Green', 'folder': '7. Green'},
        'ice': {'idle': '8. Ice.png', 'name': 'Ice', 'folder': '8. Ice'},
        'lightning': {'idle': '10. Lightning.png', 'name': 'Lightning', 'folder': '10. Lightning'},
        'golden': {'idle': '11. Golden.png', 'name': 'Golden', 'folder': '11. Golden'},
        'neptune': {'idle': '12. Neptune.png', 'name': 'Neptune', 'folder': '12. Neptune'},
        'night': {'idle': '13. Night.png', 'name': 'Night', 'folder': '13. Night'},
        'pink': {'idle': '14. Pink.png', 'name': 'Pink', 'folder': '14. Pink'},
        'rosen': {'idle': '15. Rosen.png', 'name': 'Rosen', 'folder': '15. Rosen'},
        'shark': {'idle': '16. Shark.png', 'name': 'Shark', 'folder': '16. Shark'},
        'syringe': {'idle': '17. Syringe.png', 'name': 'Syringe', 'folder': '17. Syringe'},
    }

    def __init__(self, owner=None, offset=(30, 0), weapon_type='basic'):
        self.weapon_type = weapon_type
        self.owner = owner
        self.idle_offset_x, self.idle_offset_y = offset

        # idle 상태에서 작은 검 크기
        self.idle_w, self.idle_h = 24, 100

        # attack/defense 상태에서 큰 애니메이션 크기
        # 원본 비율 550x330을 유지하면서 적당한 크기로 스케일링
        self.anim_w, self.anim_h = 300, 180  # 550:330 비율 유지 (0.6배)

        self.x, self.y = shared_state.x, shared_state.y

        # 애니메이션 제어
        self.frame = 0
        self.anim_acc = 0.0
        self.anim_fps = 30.0
        self.frame_time = 1.0 / self.anim_fps

        # 상태 관리
        self.state = 'idle'  # 'idle', 'attack', 'defense'
        self.is_playing = True  # idle부터 시작
        self.loop = True  # idle은 루프, attack/defense는 한 번만 재생

        # 공격 방향 관리 (와이퍼처럼 번갈아가며)
        self.attack_direction = 'left_to_right'  # 'left_to_right' 또는 'right_to_left'

        # 공격당 한 번만 히트 처리하기 위한 플래그
        self.has_hit = False
        self.attack_id = 0
        self.last_hit_attack_id = -1

        # 무기 이미지 로드
        self._load_weapon_images()

        self.current_frames = self.idle_img
        self.total_frames = len(self.current_frames)

    def _load_weapon_images(self):
        """현재 선택된 무기의 이미지 로드"""
        weapon_data = self.WEAPON_DATA.get(self.weapon_type, self.WEAPON_DATA['basic'])

        # idle 이미지 로드 (무기별로 다름)
        try:
            self.idle_img = [load_image(f'10.resource/{weapon_data["idle"]}')]
            self.defense_img = [load_image(f'10.resource/{weapon_data["idle"]}')]
        except Exception:
            # 로드 실패 시 기본 이미지로 폴백 (디버그 출력 제거)
            self.idle_img = [load_image('10.resource/1. Basic.png')]
            self.defense_img = [load_image('10.resource/1. Basic.png')]

        # attack 애니메이션은 무기별 폴더에서 로드
        animation_folder = f'3.animation/weapon animation/weapon/{weapon_data["folder"]}'
        try:
            self.attack_left_to_right = [
                load_image(f'{animation_folder}/attack_re_02.png'),
                load_image(f'{animation_folder}/attack_re_03.png'),
                load_image(f'{animation_folder}/attack_re_04.png'),
            ]

            self.attack_right_to_left = [
                load_image(f'{animation_folder}/attack_re_07.png'),
                load_image(f'{animation_folder}/attack_re_08.png'),
                load_image(f'{animation_folder}/attack_re_09.png')
            ]
        except Exception:
            # 애니메이션 로드 실패 시에도 기본 애니메이션으로 폴백 (디버그 출력 제거)
            self.attack_left_to_right = [
                load_image('10.resource/attack_re_02.png'),
                load_image('10.resource/attack_re_03.png'),
                load_image('10.resource/attack_re_04.png'),
            ]

            self.attack_right_to_left = [
                load_image('10.resource/attack_re_07.png'),
                load_image('10.resource/attack_re_08.png'),
                load_image('10.resource/attack_re_09.png')
            ]

    def change_weapon(self, weapon_type):
        """무기 타입 변경"""
        if weapon_type not in self.WEAPON_DATA:
            # 알 수 없는 무기 타입일 경우 조용히 무시
            return

        self.weapon_type = weapon_type
        self._load_weapon_images()

        # 현재 상태에 맞는 프레임으로 재설정
        if self.state == 'idle':
            self.current_frames = self.idle_img
        elif self.state == 'defense':
            self.current_frames = self.defense_img
        elif self.state == 'attack':
            self.current_frames = self.attack_left_to_right

        self.total_frames = len(self.current_frames)
        self.frame = min(self.frame, self.total_frames - 1)

    def set_state(self, new_state):
        """상태 변경"""
        if self.state == new_state:
            return

        self.state = new_state
        self.frame = 0
        self.anim_acc = 0.0

        if new_state == 'idle':
            self.current_frames = self.idle_img
            self.is_playing = True
            self.loop = True
            # 공격 상태가 끝난 뒤에는 히트 플래그를 초기화
            self.has_hit = False
        elif new_state == 'attack':
            # 현재 공격 방향에 따라 올바른 애니메이션 선택
            if self.attack_direction == 'left_to_right':
                self.current_frames = self.attack_left_to_right
            else:
                self.current_frames = self.attack_right_to_left
            self.is_playing = True
            self.loop = False
            # 공격 시작 시에는 아직 히트하지 않았음
            self.has_hit = False
        elif new_state == 'defense':
            self.current_frames = self.defense_img
            self.is_playing = True
            self.loop = True

        self.total_frames = len(self.current_frames)

    def attack(self):
        """z키로 공격"""
        # 공격을 시작할 때 새로운 attack_id를 부여하고 has_hit를 초기화
        self.attack_id += 1
        self.has_hit = False

        # set_state 호출 전에 attack_direction을 먼저 동기화!
        if self.owner and hasattr(self.owner, 'attack_direction'):
            self.attack_direction = self.owner.attack_direction

        self.set_state('attack')

    def defend(self):
        """x키로 방어"""
        self.set_state('defense')

    def update(self, dt):
        # owner(캐릭터)의 상태를 따라감
        if self.owner and hasattr(self.owner, 'state'):
            # 상태가 바뀌면 set_state 호출
            # (방향 동기화는 attack() 함수에서 이미 했으므로 여기서는 하지 않음)
            if self.owner.state != self.state:
                self.set_state(self.owner.state)

            # 위치 동기화: owner의 실제 좌표 사용
            owner_x = self.owner.x
            owner_y = self.owner.y

            if self.state == 'idle':
                # idle 상태: 캐릭터 손 위치
                self.x = owner_x - 15
                self.y = owner_y + 30
            elif self.state == 'attack':
                # attack 상태: 방향에 따라 다른 위치
                if self.attack_direction == 'left_to_right':
                    # 왼쪽→오른쪽 공격
                    self.x = owner_x + 4.5
                    self.y = owner_y + 35
                else:
                    # 오른쪽→왼쪽 공격
                    self.x = owner_x - 4.5
                    self.y = owner_y + 35
            else:
                # defense 등 기타 상태
                self.x = owner_x - 15
                self.y = owner_y + 30

            # 공격 상태일 때 캐릭터 프레임과 완벽하게 동기화
            if self.state == 'attack' and hasattr(self.owner, 'action_frame'):

                # 캐릭터의 action_frame을 직접 무기 프레임으로 사용 (1:1 매칭)
                self.frame = self.owner.action_frame
                if self.frame >= self.total_frames:
                    self.frame = self.total_frames - 1

        # 애니메이션 재생 (attack 상태가 아닐 때만 자동 진행)
        if self.is_playing and self.total_frames > 0 and self.state != 'attack':
            self.anim_acc += dt
            while self.anim_acc >= self.frame_time:
                self.frame += 1
                self.anim_acc -= self.frame_time

                # 프레임이 끝까지 갔을 때
                if self.frame >= self.total_frames:
                    if self.loop:
                        # idle은 반복
                        self.frame = 0
                    else:
                        # attack/defense는 끝나면 idle로 돌아감
                        self.frame = self.total_frames - 1
                        self.set_state('idle')

    def get_bb(self):
        """바운딩 박스 반환 (x1, y1, x2, y2)"""
        if self.state == 'attack':
            # 공격 시 큰 애니메이션 박스
            half_w = self.anim_w / 2
            half_h = self.anim_h / 2
            return (self.x - half_w, self.y - half_h,
                    self.x + half_w, self.y + half_h)
        elif self.state == 'defense':
            # 방어 시 가로로 긴 박스 (90도 회전)
            half_w = self.anim_w / 2  # 가로 길이
            half_h = self.idle_w / 2  # 세로 두께
            return (self.x - half_w, self.y - 20 - half_h,
                    self.x + half_w, self.y - 20 + half_h)
        else:
            # idle 상태: 작은 검
            half_w = self.idle_w / 2
            half_h = self.idle_h / 2
            return (self.x - half_w, self.y - half_h,
                    self.x + half_w, self.y + half_h)



    def draw(self):
        # 캐릭터가 스킬 사용 중이면 무기도 그리지 않음
        if self.owner and hasattr(self.owner, 'using_skill') and self.owner.using_skill:
            return

        if self.total_frames > 0:
            img = self.current_frames[self.frame]

            # 상태에 따라 다른 크기로 그리기
            if self.state == 'attack':
                # attack만 큰 애니메이션 이미지
                # current_frames가 이미 올바른 방향의 애니메이션이므로 그대로 그림
                img.draw(self.x, self.y, self.anim_w, self.anim_h)
            elif self.state =='defense':
                import math
                img.composite_draw(math.pi / 2, '', self.x, self.y-20, 24, 100)
            else:
                # idle, jump, defense는 작은 검 이미지
                img.draw(self.x, self.y, self.idle_w, self.idle_h)

        # 바운딩 박스 그리기 (디버그용)
        x1, y1, x2, y2 = self.get_bb()
        draw_rectangle(x1, y1, x2, y2)
