import pygame
import random
import math

pygame.init()

screen_width = 800
screen_height = 1000

white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("上に向かうゲーム")

#追加部分：diff
# 弾が出現する前の遅延を追跡する変数
initial_bullet_delay = 120
running = True
clock = pygame.time.Clock()
delay_timer = initial_bullet_delay  # 遅延タイマーを初期化

#プレイヤーのサイズと初期位置、移動速度を設定
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 30
player_speed = 10
speed_multiplier = 1

#弾の最大数やサイズ、速度、生成間隔を設定
max_bullets = 10
bullet_width = 10
bullet_height = 10
bullet_speed = 10

homing_bullet_turn = 0

#追加部分：diff
# ゲームの難易度設定
# create_bullet()の一度に生成する弾の数 もいじっていいかも
difficulty = input("難易度を選択してください（easy, medium, hard）: ")

if difficulty == "easy":
    max_bullets = 10
    bullet_width = 10
    bullet_height = 10
    bullet_speed = 5
    maina_speed = 0.02

elif difficulty == "medium":
    max_bullets = 15
    bullet_width = 15
    bullet_height = 15
    bullet_speed = 10
    maina_speed = 0.15


elif difficulty == "hard":
    max_bullets = 20
    bullet_width = 20
    bullet_height = 20
    bullet_speed = 15
    maina_speed = 0.2


else:
    print("無効な難易度が選択されました。デフォルトの難易度に設定します。")
    # デフォルト値を設定
    max_bullets = 10
    bullet_width = 10
    bullet_height = 10
    bullet_speed = 10


min_bullet_interval = 10  # 最小の弾の出現間隔
max_bullet_interval = 30  # 最大の弾の出現間隔
bullet_interval = 0  # 初期の出現間隔
bullet_timer = 0  # タイマー
bullets = []

# 追加部分: ポイントの初期化とポイントに関する変数
points = 0
point_font = pygame.font.Font(None, 36)

# 追加部分: 1秒ごとにポイントを増やすための変数
point_increase_timer = 0
points_per_second = 10  # 1秒ごとに増えるポイント数

# 追加部分: 赤くなる状態の関連変数
red_duration = 0
red_effect_frames = 200
red = False


blue_duration = 0
blue_effect_frames = 500
blue = False




#一定の間隔で複数の弾を生成。ランダムな位置から弾を生成し、リストbulletsに追加
def create_bullet():
    global bullet_timer, bullet_interval
    bullet_timer += 1
    if bullet_timer > bullet_interval:
        num_bullets = random.randint(1, 3)  # 一度に生成する弾の数
        for _ in range(num_bullets):
            bullet_x = random.randint(0, screen_width - bullet_width)
            bullet_y = 0
            #追加部分：diff
            if random.random() < 0.10:  # 10%の確率で"homing"ラベルを持つ弾を生成
                homing_bullet_speed = bullet_speed/1.1  # ホーミング弾の速度係数
                mai_speed = 10
                bullets.append([bullet_x, bullet_y, "homing",homing_bullet_speed,mai_speed])
            else:
                bullets.append([bullet_x, bullet_y, "normal",0,0])
        bullet_interval = random.randint(min_bullet_interval, max_bullet_interval)
        bullet_timer = 0

#追加部分：diff
# プレイヤーに向かって動く弾を生成
def create_homing_bullet():
    bullet_x = random.randint(0, screen_width - bullet_width,)
    bullet_y = 0
    bullets.append([bullet_x, bullet_y, "homing",homing_bullet_speed])

#プレイヤーと弾の衝突を判定
def is_collision(player_x, player_y, bullet_x, bullet_y, bullet_type):
    if (not red and
            player_x < bullet_x + bullet_width and
            player_x + player_width > bullet_x and
            player_y < bullet_y + bullet_height and
            player_y + player_height > bullet_y):
        return True
    return False
    

running = True
clock = pygame.time.Clock()


#プレイヤーのキー入力
#弾の生成、移動、描画、画面外に出た弾は削除
#プレイヤーと弾の衝突を検出、衝突した場合はゲームを終了。

while running:
    screen.fill(white) 

    # 弾が現れるまでの猶予
    if delay_timer > 0:
        delay_timer -= 1
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 追加部分: 1秒ごとにポイントを増やす
        point_increase_timer += 1
        if point_increase_timer == 60:  # 60フレーム = 1秒
            points += points_per_second
            point_increase_timer = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
        if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
            player_y += player_speed

        # 追加部分: スペースキーでポイントを消費して赤くなる
        if keys[pygame.K_SPACE] and points >= 20:
            points -= 20
            red = True
            red_duration = red_effect_frames

        if red:
            red_duration -= 1
            if red_duration <= 0:
                red = False

        
        # 追加部分: Shiftキーでポイントを消費して一定時間操作キャラの速度をあげる
        if keys[pygame.K_LSHIFT] and points >= 5:
            points -= 5
            blue = True
            blue_duration = blue_effect_frames
            player_speed *=1.2


        if blue:
            blue_duration -= 1
            if blue_duration <= 0:
                player_speed = 10
                blue = False

        #生成
        create_bullet()

        homing_bullet_turn += 1  # ホーミング弾のターンを増やす

       
        
        #弾の移動
        for bullet in bullets[:]:
            # 通常の弾
            if bullet[2] == "normal":
                bullet[1] += bullet_speed
            #ホーミング
            elif bullet[2] == "homing":
                # "homing" ラベルが付いた弾はプレイヤーに向かって移動
                # プレイヤーの位置と弾の位置を考慮して、弾をプレイヤーに向かって移動させる

                if homing_bullet_turn % 1 == 0:  # nターンに1度の頻度でプレイヤーを追跡する
                    homing_bullet_speed = bullet[3]  # ホーミング弾の速度係数

                    player_center_x = player_x + player_width / 2
                    player_center_y = player_y + player_height / 2

                    bullet_center_x = bullet[0] + bullet_width / 2
                    bullet_center_y = bullet[1] + bullet_height / 2

                    # ランダムな微小な角度を追加
                    angle = math.atan2(player_center_y - bullet_center_y, player_center_x - bullet_center_x)
                    angle += random.uniform(-0.1, 0.1)  # ランダムな微小な変化 (-0.2 ～ 0.2 の範囲)

                    # ランダムな速度変化を追加
                    homing_bullet_speed += random.uniform(-1, 1)  # ランダムな速度変化 (-2 ～ 2 の範囲)
            
                    if  bullet[4] <= 0:  # ホーミング弾の持続時間が終わったら、通常の弾に変更する
                        bullet[2] = "normal"
                    else:
                        bullet[4] -= maina_speed  # ホーミング弾の持続時間を減少させる
                        # プレイヤーの方向に少しずつ移動
                        angle = math.atan2(player_center_y - bullet_center_y, player_center_x - bullet_center_x)
                        bullet[0] += homing_bullet_speed * math.cos(angle)
                        bullet[1] += homing_bullet_speed * math.sin(angle)

                   

            pygame.draw.rect(screen, black, [bullet[0], bullet[1], bullet_width, bullet_height])

            if bullet[1] > screen_height:
                bullets.remove(bullet)
            
            #追加部分：diff bullet[2]
            if bullet[2] == "normal" and not red and is_collision(player_x, player_y, bullet[0], bullet[1], bullet[2]):
                running = False  # ゲームオーバー
                print("ゲームオーバー01")

            if bullet[2] == "homing" and not red and is_collision(player_x, player_y, bullet[0], bullet[1], bullet[2]):
                running = False  # ゲームオーバー
                print("ゲームオーバー02")

        

    # 追加部分: ポイント表示
    if red:
        text = point_font.render("Points: " + str(points) + " (Red for: " + str(red_duration) + " frames)", True, (255, 0, 0))
        screen.blit(text, (10, 10))
    else:
        text = point_font.render("Points: " + str(points), True, black)
        screen.blit(text, (10, 10))

    invincible_text = point_font.render("Use_Invincible/SHIFT_KYE: -20", True, (255, 0, 0))
    screen.blit(invincible_text, (10, 60))

    if blue:
        text = point_font.render("Points: " + str(points) + " (Blue for: " + str(blue_duration) + " frames)", True, (0, 0, 255))
        screen.blit(text, (10, 10))
    else:
        text = point_font.render("Points: " + str(points), True, black)
        screen.blit(text, (10, 10))

    invincible_text = point_font.render("Use_Acceleration/SPACE_KYE: -5", True, (0, 0, 255))
    screen.blit(invincible_text, (10, 90))


    pygame.draw.rect(screen, black, [player_x, player_y, player_width, player_height])
    pygame.display.update()

    clock.tick(60)

pygame.quit()