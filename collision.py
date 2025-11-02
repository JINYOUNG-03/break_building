import building
import weapon


class Collision:
    @staticmethod
    def check_weapon_building(weapon, building)::
        wx1,wx1,wx2,wy2= weapon.get_bb()
        bx1,by1,bx2,by2= building.get_bb()
        return not (wx2 < bx1 or wx1 > bx2 or wy2 < by1 or wy1 > by2)
