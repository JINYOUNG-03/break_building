from pico2d import *
from building import BuildingManager
from start import Start
from menu import GameMenu
from gamestart import GameStart
from gameover import GameOver
from character import Character
from weapon import Weapon
from collision import CollisionManager, CollisionHandler

SCREEN_H=960
SCREEN_W=540
# 전역 상태들
running = False
start_screen = None
menu = None
gamestart = None
gameover = None
character = None
weapon = None
current_screen = None
world = []
buildings = []
collision_handler = None
building_manager = None
x_pressed = False
score = 0  # 점수 추가
combo_score = 100  # 콤보 점수 (연속 파괴 시 증가)
game_time = 0  # 게임 시간 추가

def reset_world():
    global running, start_screen, menu, gamestart, gameover, character, weapon, current_screen, world, buildings, building_manager, collision_handler, x_pressed, score, combo_score, game_time
    running = True
    start_screen = Start()
    menu = GameMenu()
    gamestart = GameStart()
    gameover = GameOver()
    character = Character()
    weapon = Weapon(owner=character)  # 캐릭터를 owner로 전달
    collision_handler = CollisionHandler()  # 충돌 핸들러 초기화
    current_screen = start_screen
    world = [current_screen]
    buildings = []
    x_pressed = False
    score = 0  # 점수 초기화
    combo_score = 100  # 콤보 점수 초기화
    game_time = 0  # 게임 시간 초기화

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
    global building_manager, current_screen, gamestart, gameover, world, weapon, character, collision_handler, x_pressed, score, combo_score, game_time
    game_time += dt  # 게임 시간 업데이트

    # world 객체들 업데이트
    for obj in world:
        try:
            obj.update(dt)
        except TypeError:
            obj.update()

    # building_manager 업데이트
    if building_manager:
        building_manager.update(dt, current_screen == gamestart)

    # 게임 플레이 중일 때만 충돌 검사 및 게임오버 체크
    if current_screen == gamestart and building_manager and collision_handler and weapon and character:
        # 건물이 y좌표 110 이하로 내려가면 게임오버
        for building in building_manager.buildings:
            if building.y <= 110:
                current_screen = gameover
                world = [current_screen]
                print(f"[게임오버] 최종 점수: {score}")
                return

        # 무기-건물 충돌 검사
        weapon_collisions = CollisionManager.check_weapon_buildings(weapon, building_manager.buildings)
        # attack_id를 사용해 동일한 공격에서 중복 히트되는 것을 방지
        if weapon_collisions and hasattr(weapon, 'attack_id'):
            if getattr(weapon, 'last_hit_attack_id', -1) != weapon.attack_id:
                # 첫 충돌 객체 하나만 처리
                b = weapon_collisions[0]
                collision_handler.handle_weapon_building_collision(weapon, b)
                building_manager.destroy_building(b)
                score += combo_score  # 콤보 점수만큼 증가
                combo_score += 10  # 다음 파괴 시 10점 더 증가
                # 이번 attack_id에서 이미 히트했음을 기록
                weapon.last_hit_attack_id = weapon.attack_id
        elif weapon_collisions:
            # fallback: has_hit 플래그 사용
            if not getattr(weapon, 'has_hit', False):
                b = weapon_collisions[0]
                collision_handler.handle_weapon_building_collision(weapon, b)
                building_manager.destroy_building(b)
                score += combo_score  # 콤보 점수만큼 증가
                combo_score += 10  # 다음 파괴 시 10점 더 증가
                weapon.has_hit = True

        # 캐릭터-건물 충돌 검사
        character_collisions = CollisionManager.check_character_buildings(character, building_manager.buildings)
        for building in character_collisions:
            # 전체 빌딩 리스트와 X키 상태를 전달
            collision_handler.handle_character_building_collision(character, building, building_manager.buildings, x_pressed)

def render_world():
    global building_manager, world, score, current_screen, gamestart, gameover, game_time
    clear_canvas()
    # 배경을 먼저 그림
    for obj in world:
        obj.draw()
    # 그 다음 건물을 그림 (배경 위에 표시)
    if building_manager and current_screen == gamestart:
        building_manager.draw()

    # 게임 플레이 중일 때만 점수 및 시간 표시
    if current_screen == gamestart:
        # 점수 텍스트 표시 (왼쪽 상단)
        font = load_font('ENCR10B.TTF', 30)
        font.draw(20, SCREEN_H - 40, f'SCORE: {score}', (255, 255, 255))
        # 게임 시간 텍스트 표시 (오른쪽 상단)
        font.draw(SCREEN_W - 200, SCREEN_H - 40, f'TIME: {int(game_time)}s', (255, 255, 255))

    # 게임오버 화면일 때 최종 점수 표시
    if current_screen == gameover:
        font = load_font('ENCR10B.TTF', 40)
        font.draw(SCREEN_W // 2 - 120, SCREEN_H // 2, f'FINAL SCORE: {score}', (255, 0, 0))

    update_canvas()

def handle_events():
    """입력 처리: ESC/QUIT은 종료, 화면 전환(예: m/s/r), gamestart에서만 캐릭터 조작, 'b'는 빌딩 낙하 트리거."""
    global running, current_screen, world, start_screen, menu, gamestart, gameover, character, weapon, x_pressed, combo_score, score, building_manager
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
                # gamestart로 진입하면 빌딩 낙하 시작 및 난이도 리셋
                if building_manager:
                    building_manager.clear()  # 기존 건물 제거 및 난이도 리셋
                score = 0  # 점수 초기화
                combo_score = 100  # 콤보 점수 초기화
                start_all_buildings()
                continue
            if current_screen == gamestart and event.key == SDLK_r:
                current_screen = start_screen
                world = [current_screen]
                # 게임 화면에서 나갈 때 건물 제거 및 난이도 리셋
                if building_manager:
                    building_manager.clear()
                continue
            # 게임오버 화면에서 r키로 재시작
            if current_screen == gameover and event.key == SDLK_r:
                current_screen = menu
                world = [current_screen]
                if building_manager:
                    building_manager.clear()
                score = 0
                combo_score = 100
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
                    combo_score = 100  # 방어 상태로 전환 시 콤보 점수 리셋
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
