import os
import pygame

pygame.init()

score = 0
lives = 2

screen_width = 640 
screen_height = 360 
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀
pygame.display.set_caption("TEAM_FIVE")

# FPS
clock = pygame.time.Clock()


#사용자 게임 초기화
current_path = os.path.dirname(__file__) # 현재 파일의 위치 반환
image_path = r= os.path.join(current_path, "images")
 # images 폴더 위치 반환

# 배경
background = pygame.image.load(os.path.join(image_path, "background.png"))

#stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#character
# 캐릭터 만들기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height


character_to_x = 0
character_speed = 5

# weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 10

# 공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9] 

# 공들
balls = []


# 최초 발생하는 큰 공 추가
balls.append({
    "pos_x" : 50, 
    "pos_y" : 50, 
    "img_idx" : 0, 
    "to_x": 3, 
    "to_y": -6, 
    "init_spd_y": ball_speed_y[0]})

# 사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

#font
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()

#score location
score_font = pygame.font.Font(None, 50)
score_x_pos = screen_width - 10 - score_font.size("Score: 0")[0]
score_y_pos = 10

#게임 속도에 따른 설정
def set_level(score, balls):
    if score < 50:
        level = 1
        speed = 2
    elif score < 100:
        level = 2
        speed = 4
    elif score < 150:
        level = 3
        speed = 6
    else:
        level = 4
        speed = 8
    
    for ball in balls:
        ball['to_y'] = speed
    return level

game_result = "Game Over"


running = True
while running:
    dt = clock.tick(30)
    
    # 2. 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: 
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # 무기 위치
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons]

    # 천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
    

    # 공 위치 정의
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # 가로벽에 닿았을 때 공 이동 위치 변경 (튕겨 나오는 효과)
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        # 세로 위치
        # 스테이지에 튕겨서 올라가는 처리
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else: # 그 외의 모든 경우에는 속도를 증가
            ball_val["to_y"] += 0.5

        if ball_img_idx == 3 and ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["img_idx"] = 0
            ball_val["to_x"] = 3
            ball_val["to_y"] = -6
            ball_val["init_spd_y"] = ball_speed_y[0]

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        # 공 rect 정보 업데이트
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # 공과 캐릭터 충돌 체크
        if character_rect.colliderect(ball_rect):
            lives -= 1  # 목숨 감소
            if lives <= 0:
                running = False
            else:
                # 게임 재시작 로직
                character_x_pos = (screen_width / 2) - (character_width / 2)
                character_y_pos = screen_height - character_height - stage_height
                character_to_x = 0
                weapons = []
                balls = []
                balls.append({
                    "pos_x" : 50,
                    "pos_y" : 50,
                    "img_idx" : 0,
                    "to_x": 3,
                    "to_y": -6,
                    "init_spd_y": ball_speed_y[0]
                })
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # 무기 rect 정보 업데이트
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # 충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx 
                ball_to_remove = ball_idx 
                
                #가장 작은 크기의 공이 아니면 다음 단계의 공으로 나누기
                if ball_img_idx<3:
                    #현재 공 크기 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]
                    
                    #나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]
                    
                    #왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,
                        "to_x": -3,
                        "to_y":-6,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]
                    })
                    
                    #오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx": ball_img_idx + 1,
                        "to_x": 3,
                        "to_y":-6,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]
                    })
                score += 20
                break
            else:
                continue
            break
    

    # 충돌된 공 or 무기 없애기
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
        score += 20

        level = set_level(score, balls)

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1
    
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_pos, character_y_pos))
    
    #경과 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10,10))

    # 목숨 표시
    lives_render = game_font.render("Lives: {}".format(lives), True, (255, 255, 255))
    screen.blit(lives_render, (10, 50))

    pygame.display.update()
    
    #점수 표시
    score_render = game_font.render("Score: {}".format(score), True, (255, 255, 255))
    screen.blit(score_render, (score_x_pos, score_y_pos))
    
    #시간 초과
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        funning = False
    
    pygame.display.update()

#게임오버메시지
if not running:
    msg = game_font.render(game_result, True, (255,255,0))
    msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
    screen.blit(msg, msg_rect)
    
    # 점수 표시
    score_result = game_font.render("Score: {}".format(score), True, (255, 255, 255)) 
    score_rect = score_result.get_rect(center=(int(screen_width / 2), int(screen_height / 2) + 50))
    screen.blit(score_result, score_rect)
    
    
pygame.display.update()

pygame.time.delay(2000)

pygame.quit()