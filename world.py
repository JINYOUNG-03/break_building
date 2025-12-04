from pico2d import *
from building import BuildingManager
from start import Start
from menu import GameMenu
from gamestart import GameStart
from gameover import GameOver
from character import Character
from weapon import Weapon
from collision import CollisionManager, CollisionHandler
from tutorial import Tutorial
from missile import MissileManager
from weapon_select import WeaponSelect
from fragment import FragmentManager

SCREEN_H=960
SCREEN_W=540
# 전역 상태들
running = False
start_screen = None
menu = None
gamestart = None
gameover = None
tutorial = None
weapon_select = None
character = None
weapon = None
current_screen = None
world = []
buildings = []
collision_handler = None
building_manager = None
missile_manager = None
fragment_manager = None
x_pressed = False
score = 0  # 점수 추가
combo_score = 100  # 콤보 점수 (연속 파괴 시 증가)
game_time = 0  # 게임 시간 추가
buildings_destroyed = 0  # 파괴된 건물 수 추가
selected_weapon_id = 'basic'  # 선택된 무기 ID 추가
combo_count = 0  # 콤보 카운트 추가
combo_images = []  # 콤보 이미지 리스트
menu_music = None
gameplay_music = None
current_music = 'menu'
destruct_sound = None

def reset_world():
    global running, start_screen, menu, gamestart, gameover, tutorial, weapon_select, character, weapon, current_screen, world, buildings, building_manager, collision_handler, missile_manager, fragment_manager, x_pressed, score, combo_score, game_time, selected_weapon_id, combo_count, combo_images, menu_music, gameplay_music, current_music, destruct_sound
    running = True
    start_screen = Start()
    menu = GameMenu()
    gamestart = GameStart()
    gameover = GameOver()
    tutorial = Tutorial()
    weapon_select = WeaponSelect()
    character = Character()
    weapon = Weapon(owner=character)  # 캐릭터를 owner로 전달
    collision_handler = CollisionHandler()  # 충돌 핸들러 초기화
    missile_manager = MissileManager(
        spawn_interval=6.0,
        spawn_x_min=60,
        spawn_x_max=480,
        spawn_y=950,
        speed=300.0
    )

    # FragmentManager 초기화
    fragment_manager = FragmentManager()

    # 콤보 이미지 로드
    combo_images = []
    for i in range(10):
        try:
            img = load_image(f'10.resource/damage1_0{i}.png')
            combo_images.append(img)
        except:
            combo_images.append(None)

    # 음악 및 효과음 로드
    try:
        menu_music = load_music('10.resource/menu_music.mp3')
        gameplay_music = load_music('10.resource/gameplay_music.mp3')
        destruct_sound = load_wav('10.resource/destruct.wav')
    except:
        print("음악/효과음 파일을 찾을 수 없습니다.")

    current_screen = start_screen
    world = [current_screen]
    buildings = []
    x_pressed = False
    score = 0  # 점수 초기화
    combo_score = 100  # 콤보 점수 초기화
    game_time = 0  # 게임 시간 초기화
    selected_weapon_id = 'basic'  # 선택된 무기 ID 초기화
    combo_count = 0  # 콤보 카운트 초기화

    # 메뉴 음악 재생 (무한 반복)
    if menu_music:
        menu_music.set_volume(50)
        menu_music.repeat_play()
    current_music = 'menu'

    # BuildingManager 초기화
    building_manager = BuildingManager(
        spawn_interval=1.5,
        spawn_x=270,
        spawn_y=800,  # 화면 안에서 시작하도록 낮춤
        fall_speed=200.0,
        screen_bottom=0
    )

def switch_music(music_type):
    """배경음악 전환 함수"""
    global menu_music, gameplay_music, current_music

    if current_music == music_type:
        return  # 이미 재생 중이면 아무것도 하지 않음

    # 모든 음악 정지
    if menu_music:
        menu_music.stop()
    if gameplay_music:
        gameplay_music.stop()

    # 새로운 음악 재생
    if music_type == 'menu' and menu_music:
        menu_music.repeat_play()
        current_music = 'menu'
    elif music_type == 'gameplay' and gameplay_music:
        gameplay_music.repeat_play()
        current_music = 'gameplay'

def start_all_buildings():
    global building_manager
    if building_manager:
        building_manager.start_all()

def manual_spawn_building():
    """b키로 수동 빌딩 스폰"""
    global building_manager
    if building_manager:
        building_manager.manual_spawn()

def manual_spawn_missile():
    """m키로 수동 미사일 스폰"""
    global missile_manager
    if missile_manager:
        import random
        x = random.uniform(missile_manager.spawn_x_min, missile_manager.spawn_x_max)
        from missile import Missile
        m = Missile(x, missile_manager.spawn_y, missile_manager.speed)
        missile_manager.missiles.append(m)
        print(f"[Manual] Spawned missile at x={x}, y={missile_manager.spawn_y}")

def update_world(dt):
    global building_manager, missile_manager, fragment_manager, current_screen, gamestart, gameover, world, weapon, character, collision_handler, x_pressed, score, combo_score, game_time, buildings_destroyed, combo_count, destruct_sound
    if current_screen == gamestart:
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

    # missile_manager 업데이트
    if missile_manager:
        missile_manager.update(dt, current_screen == gamestart)

    # 게임 플레이 중일 때만 충돌 검사 및 게임오버 체크
    if current_screen == gamestart and building_manager and collision_handler and weapon and character:
        # 건물이 y좌표 110 이하로 내려가면 게임오버
        for building in building_manager.buildings:
            if building.y <= 110:
                current_screen = gameover
                world = [current_screen]
                return

        # 무기-건물 충돌 검사
        weapon_collisions = CollisionManager.check_weapon_buildings(weapon, building_manager.buildings)
        # attack_id를 사용해 동일한 공격에서 중복 히트되는 것을 방지
        if weapon_collisions and hasattr(weapon, 'attack_id'):
            if getattr(weapon, 'last_hit_attack_id', -1) != weapon.attack_id:
                # 첫 충돌 객체 하나만 처리
                b = weapon_collisions[0]
                collision_handler.handle_weapon_building_collision(weapon, b)
                # 건물에 히트 처리: 첫 히트는 손상 이미지로 변경, 두 번째는 파괴
                destroyed = b.hit()
                if destroyed:
                    # 파편 생성 (건물 위치에서)
                    if fragment_manager:
                        fragment_manager.create_fragments(b.x, b.y, count=5)
                    building_manager.destroy_building(b)
                    if destruct_sound:
                        destruct_sound.play()  # 건물 파괴 효과음 재생
                    score += combo_score  # 콤보 점수만큼 증가
                    combo_score += 10  # 다음 파괴 시 10점 더 증가
                    buildings_destroyed += 1  # 파괴된 건물 수 증가
                    combo_count += 1  # 콤보 카운트 증가
                # 이번 attack_id에서 이미 히트했음을 기록
                weapon.last_hit_attack_id = weapon.attack_id
        elif weapon_collisions:
            # fallback: has_hit 플래그 사용
            if not getattr(weapon, 'has_hit', False):
                b = weapon_collisions[0]
                collision_handler.handle_weapon_building_collision(weapon, b)
                destroyed = b.hit()
                if destroyed:
                    # 파편 생성 (건물 위치에서)
                    if fragment_manager:
                        fragment_manager.create_fragments(b.x, b.y, count=5)
                    building_manager.destroy_building(b)
                    if destruct_sound:
                        destruct_sound.play()  # 건물 파괴 효과음 재생
                    score += combo_score  # 콤보 점수만큼 증가
                    combo_score += 10  # 다음 파괴 시 10점 더 증가
                    buildings_destroyed += 1  # 파괴된 건물 수 증가
                    combo_count += 1  # 콤보 카운트 증가
                weapon.has_hit = True

        # 캐릭터-건물 충돌 검사
        character_collisions = CollisionManager.check_character_buildings(character, building_manager.buildings)
        for building in character_collisions:
            # 전체 빌딩 리스트와 X키 상태, dt를 전달
            collision_handler.handle_character_building_collision(character, building, building_manager.buildings, x_pressed, dt)

        # 미사일-캐릭터 충돌 검사
        if missile_manager:
            collided_missiles = CollisionManager.check_missiles_character(missile_manager.missiles, character)
            if collided_missiles:
                try:
                    missile_manager.remove(collided_missiles[0])
                except Exception:
                    pass
                current_screen = gameover
                world = [current_screen]
                return

def render_world():
    global building_manager, missile_manager, fragment_manager, world, score, current_screen, gamestart, gameover, game_time, combo_count, combo_images
    clear_canvas()
    # 배경을 먼저 그림
    for obj in world:
        obj.draw()
    # 그 다음 건물을 그림 (배경 위에 표시)
    if building_manager and current_screen == gamestart:
        building_manager.draw()

    # 미사일 그리기
    if missile_manager and current_screen == gamestart:
        missile_manager.draw()

    # 파편 그리기
    if fragment_manager and current_screen == gamestart:
        fragment_manager.draw()


    # 게임 플레이 중일 때만 점수 및 시간 표시
    if current_screen == gamestart:
        # 점수 텍스트 표시 (왼쪽 상단)
        font = load_font('ENCR10B.TTF', 30)
        font.draw(20, SCREEN_H - 40, f'SCORE: {score}', (255, 255, 255))
        # 게임 시간 텍스트 표시 (오른쪽 상단)
        font.draw(SCREEN_W - 200, SCREEN_H - 40, f'TIME: {int(game_time)}s', (255, 255, 255))

        # 콤보 카운트 이미지 표시 (캐릭터 오른쪽 위)
        if combo_count > 0 and combo_images and character:
            # 두 자리수 표현: 99까지 표시 가능
            display_combo = min(combo_count, 99)

            if display_combo < 10:
                # 한 자리수: 해당 숫자 이미지 하나만 표시
                # combo_count 1 -> 인덱스 1 (damage1_02.png)
                combo_img = combo_images[display_combo]
                combo_img.draw(character.x + 60, character.y + 80)
            else:
                # 두 자리수: 십의 자리와 일의 자리를 각각 표시
                tens_digit = display_combo // 10
                ones_digit = display_combo % 10

                # 십의 자리 숫자
                tens_img = combo_images[tens_digit]
                tens_img.draw(character.x + 40, character.y + 80)

                # 일의 자리 숫자
                ones_img = combo_images[ones_digit]
                ones_img.draw(character.x + 80, character.y + 80)

    # 게임오버 화면일 때 최종 점수 및 파괴한 건물 수 표시
    if current_screen == gameover:
        font = load_font('ENCR10B.TTF', 30)
        font.draw(150, SCREEN_H // 2 + 130, f'Destroy buildings: {buildings_destroyed}', (255, 255, 0))
        font.draw(SCREEN_W // 2 - 100, SCREEN_H // 2+ 30, f'FINAL SCORE: {score}', (255, 0, 0))
        font.draw(160,430, f'Play time: {int(game_time//1)} seconds', (255, 255, 255))

    update_canvas()

def handle_events():
    """입력 처리: ESC/QUIT은 종료, 화면 전환(예: m/s/r), gamestart에서만 캐릭터 조작, 'b'는 빌딩 낙하 트리거."""
    global running, current_screen, world, start_screen, menu, gamestart, gameover, tutorial, weapon_select, character, weapon, x_pressed, combo_score, score, building_manager, missile_manager, game_time, buildings_destroyed, combo_count, selected_weapon_id
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
            continue
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
                continue
            # gamestart 화면에서만 캐릭터 조작 허용
            if current_screen == gamestart:
                if event.key == SDLK_LEFT:
                    character.move_left()
                elif event.key == SDLK_RIGHT:
                    character.move_right()
                elif event.key == SDLK_b:
                    manual_spawn_building()
                elif event.key == SDLK_m:  # m키로 미사일 수동 스폰
                    manual_spawn_missile()
                elif event.key == SDLK_z:
                    character.attack()
                    weapon.attack()
                elif event.key == SDLK_x:
                    # X키 누름 상태를 기록
                    x_pressed = True
                    character.defend()
                    weapon.defend()
                    combo_score = 100  # 방어 상태로 전환 시 콤보 점수 리셋
                    combo_count = 0  # 방어 시 콤보 카운트 0으로 초기화
                continue
            # 다른 화면에서 처리할 키가 있으면 여기 추가
        if event.type == SDL_KEYUP:
            # 키가 떼어졌을 때 X키 상태 초기화
            if event.key == SDLK_x:
                x_pressed = False
            continue
        if event.type == SDL_MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.x, SCREEN_H - event.y

            # start_screen에서 클릭 처리
            if current_screen == start_screen:
                # start 버튼 클릭 시 menu로 이동
                if hasattr(start_screen, 'check_button_click'):
                    result = start_screen.check_button_click(mouse_x, mouse_y)
                    if result == 'start':
                        current_screen = menu
                        world = [current_screen]
                        continue

            # menu에서 클릭 처리
            elif current_screen == menu:
                if hasattr(menu, 'check_button_click'):
                    result = menu.check_button_click(mouse_x, mouse_y)
                    if result == 'play':
                        current_screen = gamestart
                        world = [current_screen, character, weapon]
                        if building_manager:
                            building_manager.clear()
                        if missile_manager:
                            missile_manager.clear()
                        score = 0
                        combo_score = 100
                        game_time = 0
                        buildings_destroyed = 0
                        combo_count = 0  # 콤보 카운트 초기화
                        start_all_buildings()
                        continue
                    elif result == 'tutorial':
                        current_screen = tutorial
                        world = [current_screen]
                        continue
                    elif result == 'weapon':
                        current_screen = weapon_select
                        world = [current_screen]
                        continue
                    elif result == 'quit':
                        running = False
                        continue

            # weapon_select에서 클릭 처리
            elif current_screen == weapon_select:
                if hasattr(weapon_select, 'check_button_click'):
                    action, value = weapon_select.check_button_click(mouse_x, mouse_y)
                    if action == 'back':
                        current_screen = menu
                        world = [current_screen]
                        continue
                    elif action == 'confirm':
                        selected_weapon_id = value
                        print(f"Selected weapon: {selected_weapon_id}")
                        # TODO: 나중에 weapon.change_weapon(selected_weapon_id) 구현
                        current_screen = menu
                        world = [current_screen]
                        continue
                    elif action == 'weapon':
                        # 무기 선택만 하고 화면은 유지
                        pass

            # tutorial에서 클릭 처리
            elif current_screen == tutorial:
                if hasattr(tutorial, 'check_button_click'):
                    result = tutorial.check_button_click(mouse_x, mouse_y)
                    if result == 'back':
                        current_screen = menu
                        world = [current_screen]
                        continue

            # gameover에서 클릭 처리
            elif current_screen == gameover:
                if hasattr(gameover, 'check_button_click'):
                    result = gameover.check_button_click(mouse_x, mouse_y)
                    if result == 'restart':
                        current_screen = menu
                        world = [current_screen]
                        if building_manager:
                            building_manager.clear()
                        if missile_manager:
                            missile_manager.clear()
                        score = 0
                        combo_score = 100
                        game_time = 0
                        buildings_destroyed = 0
                        combo_count = 0  # 콤보 카운트 초기화
                        continue
