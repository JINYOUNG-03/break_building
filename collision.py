"""
충돌 처리 매니저
"""

class CollisionManager:
    @staticmethod
    def check_collision(bb1, bb2):
        """
        두 바운딩 박스의 충돌 여부 확인
        bb1, bb2: (x1, y1, x2, y2) 형태의 튜플
        """
        x1_min, y1_min, x1_max, y1_max = bb1
        x2_min, y2_min, x2_max, y2_max = bb2

        # AABB (Axis-Aligned Bounding Box) 충돌 검사
        if x1_max < x2_min or x1_min > x2_max:
            return False
        if y1_max < y2_min or y1_min > y2_max:
            return False
        return True

    @staticmethod
    def check_weapon_building(weapon, building):
        """
        무기와 건물의 충돌 검사
        공격 상태일 때만 충돌 체크
        """
        if weapon.state != 'attack':
            return False

        weapon_bb = weapon.get_bb()
        building_bb = building.get_bb()

        return CollisionManager.check_collision(weapon_bb, building_bb)

    @staticmethod
    def check_character_building(character, building):
        """
        캐릭터와 건물의 충돌 검사
        """
        char_bb = character.get_bb()
        building_bb = building.get_bb()

        return CollisionManager.check_collision(char_bb, building_bb)

    @staticmethod
    def check_weapon_buildings(weapon, buildings):
        """
        무기와 여러 건물들의 충돌 검사
        충돌한 건물 리스트 반환
        """
        collided_buildings = []
        for building in buildings:
            if CollisionManager.check_weapon_building(weapon, building):
                collided_buildings.append(building)
        return collided_buildings

    @staticmethod
    def check_character_buildings(character, buildings):
        """
        캐릭터와 여러 건물들의 충돌 검사
        충돌한 건물 리스트 반환
        """
        collided_buildings = []
        for building in buildings:
            if CollisionManager.check_character_building(character, building):
                collided_buildings.append(building)
        return collided_buildings

    @staticmethod
    def check_missile_character(missile, character):
        """
        단일 미사일과 캐릭터의 충돌 검사
        """
        if not missile:
            return False
        return CollisionManager.check_collision(missile.get_bb(), character.get_bb())

    @staticmethod
    def check_missiles_character(missiles, character):
        """
        여러 미사일과 캐릭터의 충돌 검사
        충돌한 미사일 리스트 반환
        """
        collided = []
        for m in missiles:
            if CollisionManager.check_missile_character(m, character):
                collided.append(m)
        return collided


class CollisionHandler:
    """충돌 발생 시 처리를 담당하는 클래스"""

    def __init__(self):
        self.collision_count = 0  # 디버그용 충돌 카운트
        self.push_speed = 8000.0  # 빌딩을 위로 밀어올리는 속도 (pixels per second) - 방어 시 빠르게 위로 이동

    def handle_weapon_building_collision(self, weapon, building):
        """
        무기-건물 충돌 처리
        건물에 데미지를 주거나 파괴 효과 등을 여기서 처리
        """
        self.collision_count += 1
        return True

    def _move_buildings_up(self, buildings, dy):
        """
        빌딩들을 화면에서 위로 dy 픽셀만큼 이동시킴.
        dy는 양수(위로 이동시키는 픽셀 수)
        """
        if not buildings or dy <= 0:
            return

        for b in buildings:
            # 우선 move(dx, dy) 메서드가 있으면 사용
            move_fn = getattr(b, 'move', None)
            if callable(move_fn):
                try:
                    move_fn(0, dy)
                    continue
                except Exception:
                    pass

            # y 같은 속성이 있으면 직접 조정
            for attr in ('y', 'pos_y', 'y_pos', 'py'):
                if hasattr(b, attr):
                    try:
                        current = getattr(b, attr)
                        setattr(b, attr, current + dy)
                        break
                    except Exception:
                        continue
            else:
                # get_bb/set_bb 방식으로 조정 가능하면 사용
                if hasattr(b, 'get_bb') and hasattr(b, 'set_bb'):
                    try:
                        x1, y1, x2, y2 = b.get_bb()
                        b.set_bb((x1, y1 + dy, x2, y2 + dy))
                    except Exception:
                        # 변경 불가하면 무시
                        pass
        # 이동 후 겹침 해소
        self._separate_overlapping_buildings(buildings)

    def _separate_overlapping_buildings(self, buildings, min_gap=10):
        """겹친 건물들을 분리합니다"""
        if not buildings:
            return

        # Y 좌표 기준으로 정렬 (위에서 아래로)
        sorted_buildings = sorted(buildings, key=lambda b: getattr(b, 'y', 0), reverse=True)

        for i in range(len(sorted_buildings) - 1):
            b1 = sorted_buildings[i]
            b2 = sorted_buildings[i + 1]

            try:
                bb1 = b1.get_bb()
                bb2 = b2.get_bb()

                x1_1, y1_1, x2_1, y2_1 = bb1
                x1_2, y1_2, x2_2, y2_2 = bb2

                # Y축에서 겹치는지 확인
                overlap = y1_1 - (y2_2 + min_gap)

                if overlap < 0:  # 겹침 발생
                    # 아래 건물을 더 아래로 밀어냄
                    push_down = abs(overlap)
                    if hasattr(b2, 'y'):
                        b2.y -= push_down
            except Exception:
                continue

    def handle_character_building_collision(self, character, building, buildings=None, x_pressed=False, dt=0.0):
        """
        캐릭터-건물 충돌 처리
        - buildings: 전체 빌딩 리스트(있을 때 X키 누름 시 전체를 위로 이동)
        - x_pressed: X키가 눌렸는지 여부
        - dt: 프레임 델타타임(초)

        반환값: 충돌로 인한 처리 발생 여부 (True/False)
        """
        # 방어 상태면 건물들이 위로 이동함
        if getattr(character, 'state', None) == 'defense':
            # X키가 눌렸고 전체 빌딩 리스트가 주어졌으면 빌딩들을 위로 이동
            if x_pressed and buildings and dt > 0:
                # dt 기반 속도로 이동량 계산
                push_amount = self.push_speed * dt
                self._move_buildings_up(buildings, push_amount)
                return True

            # 방어 성공(하지만 이동 없음)
            return False
