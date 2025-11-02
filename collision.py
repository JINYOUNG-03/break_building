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


class CollisionHandler:
    """충돌 발생 시 처리를 담당하는 클래스"""

    def __init__(self):
        self.collision_count = 0  # 디버그용 충돌 카운트

    def handle_weapon_building_collision(self, weapon, building):
        """
        무기-건물 충돌 처리
        건물에 데미지를 주거나 파괴 효과 등을 여기서 처리
        """
        self.collision_count += 1
        print(f"[충돌] 무기가 건물을 공격! (총 {self.collision_count}회)")

        # 여기에 건물 데미지 로직 추가
        # 예: building.take_damage(10)
        # 예: building.hp -= 10

        return True

    def _move_buildings_up(self, buildings, dy):
        """
        빌딩들을 화면에서 위로 dy 픽셀만큼 이동시킴.
        다양한 빌딩 인터페이스를 지원:move(dx, dy), y 속성, get_bb/set_bb 등.
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

    def handle_character_building_collision(self, character, building, buildings=None, x_pressed=False):
        """
        캐릭터-건물 충돌 처리
        - buildings: 전체 빌딩 리스트(있을 때 X키 누름 시 전체를 위로 이동)
        - x_pressed: X키가 눌렸는지 여부

        반환값: 충돌로 인한 처리 발생 여부 (True/False)
        """
        # 방어 상태면 건물들이 위로 이동함
        if getattr(character, 'state', None) == 'defense':
            # X키가 눌렸고 전체 빌딩 리스트가 주어졌으면 빌딩들을 위로 이동
            if x_pressed and buildings:
                push_amount = 150  # 위로 이동 픽셀 수 (필요하면 조정)
                self._move_buildings_up(buildings, push_amount)
                print(f"  → 방어 및 반격: 전체 빌딩을 위로 {push_amount} 이동")
                return True

            print("  → 방어 성공!")
            return False


