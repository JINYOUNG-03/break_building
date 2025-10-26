from pico2d import *
import random
from building import BuildingManager
from start import Start
from menu import GameMenu
from gamestart import GameStart
from character import Character
from weapon import Weapon

SCREEN_H=960
# 전역 상태들
running = False
start_screen = None
menu = None
gamestart = None
character = None
current_screen = None
world = []
buildings = []
building_manager = None

def reset_world():
    global running, start_screen, menu, gamestart, character, current_screen, world, buildings, building_manager,weapon
    running = True
    start_screen = Start()
    menu = GameMenu()
    gamestart = GameStart()
    character = Character()
    current_screen = start_screen
    world = [current_screen]
    buildings = []

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
    global building_manager, current_screen, gamestart, world
    # world 객체들 업데이트
    for obj in world:
        try:
            obj.update(dt)
        except TypeError:
            obj.update()
    # building_manager 업데이트
    if building_manager:
        building_manager.update(dt, current_screen == gamestart)

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
    global running, current_screen, world, start_screen, menu, gamestart, character
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
                world = [current_screen, character]
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
                elif event.key in (SDLK_SPACE, SDLK_w, SDLK_UP):
                    character.jump()
                elif event.key == SDLK_b:
                    manual_spawn_building()
                continue
            # 다른 화면에서 처리할 키가 있으면 여기 추가
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


