from pico2d import *
from building import BuildingManager
from start import Start
from menu import GameMenu
from gamestart import GameStart
from character import Character
from weapon import Weapon
from collision import CollisionManager, CollisionHandler

SCREEN_H=960
# 전역 상태들
running = False
start_screen = None
menu = None
gamestart = None
character = None
weapon = None
current_screen = None
world = []
buildings = []
collision_handler = None
building_manager = None
x_pressed = False

def reset_world():
    global running, start_screen, menu, gamestart, character, weapon, current_screen, world, buildings, building_manager, collision_handler, x_pressed
    running = True
    start_screen = Start()
    menu = GameMenu()
    gamestart = GameStart()
    character = Character()
    weapon = Weapon(owner=character)  # 캐릭터를 owner로 전달
    collision_handler = CollisionHandler()  # 충돌 핸들러 초기화
    current_screen = start_screen
    world = [current_screen]
    buildings = []
    x_pressed = False

    # BuildingManager 초기화
    building_manager = BuildingManager(
        spawn_interval=1.5,
        spawn_x=270,
        spawn_y=800,  # 화면 안에서 시작하도록 낮춤
        fall_speed=200.0,
        screen_bottom=0
    )

def start_all_buildings():
    global building_manager
    if building_manager:
        building_manager.start_all()

def manual_spawn_building():
    """b키로 수동 빌딩 스폰"""
    global building_manager
    if building_manager:
        building_manager.manual_spawn()

def update_world(dt):
    global building_manager, current_screen, gamestart, world, weapon, character, collision_handler, x_pressed
    # world 객체들 업데이트
    for obj in world:
        try:
            obj.update(dt)
        except TypeError:
            obj.update()

    # building_manager 업데이트
    if building_manager:
        building_manager.update(dt, current_screen == gamestart)

    # 게임 플레이 중일 때만 충돌 검사
    if current_screen == gamestart and building_manager and collision_handler and weapon and character:
        # 무기-건물 충돌 검사
        weapon_collisions = CollisionManager.check_weapon_buildings(weapon, building_manager.buildings)
        # attack_id를 사용해 동일한 공격에서 중복 히트되는 것을 방지
        if weapon_collisions and hasattr(weapon, 'attack_id'):
            if getattr(weapon, 'last_hit_attack_id', -1) != weapon.attack_id:
                # 첫 충돌 객체 하나만 처리
                b = weapon_collisions[0]
                collision_handler.handle_weapon_building_collision(weapon, b)
                building_manager.destroy_building(b)
                # 이번 attack_id에서 이미 히트했음을 기록
                weapon.last_hit_attack_id = weapon.attack_id
        elif weapon_collisions:
            # fallback: has_hit 플래그 사용
            if not getattr(weapon, 'has_hit', False):
                b = weapon_collisions[0]
                collision_handler.handle_weapon_building_collision(weapon, b)
                building_manager.destroy_building(b)
                weapon.has_hit = True

        # 캐릭터-건물 충돌 검사
        character_collisions = CollisionManager.check_character_buildings(character, building_manager.buildings)
        for building in character_collisions:
            # 전체 빌딩 리스트와 X키 상태를 전달
            collision_handler.handle_character_building_collision(character, building, building_manager.buildings, x_pressed)
            # 충돌한 건물 제거 (옵션)
            # building_manager.buildings.remove(building)

def render_world():
    global building_manager, world
    clear_canvas()
    # 배경을 먼저 그림
    for obj in world:
        obj.draw()
    # 그 다음 건물을 그림 (배경 위에 표시)
    if building_manager:
        building_manager.draw()
    update_canvas()

def handle_events():
    """입력 처리: ESC/QUIT은 종료, 화면 전환(예: m/s/r), gamestart에서만 캐릭터 조작, 'b'는 빌딩 낙하 트리거."""
    global running, current_screen, world, start_screen, menu, gamestart, character, weapon, x_pressed
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
            continue
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
                continue
            # 화면 전환 단축키
            if current_screen == start_screen and event.key == SDLK_m:
                current_screen = menu
                world = [current_screen]
                continue
            if current_screen == menu and event.key == SDLK_s:
                current_screen = gamestart
                world = [current_screen, character,weapon]
                # gamestart로 진입하면 빌딩 낙하 시작
                start_all_buildings()
                continue
            if current_screen == gamestart and event.key == SDLK_r:
                current_screen = start_screen
                world = [current_screen]
                continue
            # gamestart 화면에서만 캐릭터 조작 허용
            if current_screen == gamestart:
                if event.key in (SDLK_LEFT, SDLK_a):
                    character.move_left()
                elif event.key in (SDLK_RIGHT, SDLK_d):
                    character.move_right()
                elif event.key == SDLK_b:
                    manual_spawn_building()
                elif event.key == SDLK_z:
                    character.attack()
                    weapon.attack()
                elif event.key == SDLK_x:
                    # X키 누름 상태를 기록
                    x_pressed = True
                    character.defend()
                    weapon.defend()
                continue
            # 다른 화면에서 처리할 키가 있으면 여기 추가
        if event.type == SDL_KEYUP:
            # 키가 떼어졌을 때 X키 상태 초기화
            if event.key == SDLK_x:
                x_pressed = False
            continue
        if event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, SCREEN_H - event.y
            print(f"Mouse down: ({x}, {y})")
        elif event.type == SDL_MOUSEBUTTONUP:
            x, y = event.x, SCREEN_H - event.y
            print(f"Mouse up: ({x}, {y})")
        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x, SCREEN_H - event.y
            print(f"Mouse move: ({x}, {y})")
            # 마우스 처리
