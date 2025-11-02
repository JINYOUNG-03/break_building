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

    def handle_character_building_collision(self, character, building):
        """
        캐릭터-건물 충돌 처리
        게임 오버나 캐릭터 데미지 등을 여기서 처리
        """
        # 방어 상태면 데미지 감소 또는 무시
        if character.state == 'defense':
            print("  → 방어 성공! 데미지 무시")
            return False

