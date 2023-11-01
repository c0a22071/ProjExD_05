print("hello world")
import pygame as pg
import random

pg.init()

screen_width = 800
screen_height = 1000

white = (255, 255, 255)
black = (0, 0, 0)

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("上に向かうゲーム")

#プレイヤーのサイズと初期位置、移動速度を設定
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 30
player_speed = 10

#弾の最大数やサイズ、速度、生成間隔を設定
max_bullets = 10
bullet_width = 10
bullet_height = 10
bullet_speed = 10

min_bullet_interval = 10  # 最小の弾の出現間隔
max_bullet_interval = 30  # 最大の弾の出現間隔
bullet_interval = 0  # 初期の出現間隔
bullet_timer = 0  # タイマー
bullets = []





#一定の間隔で複数の弾を生成。ランダムな位置から弾を生成し、リストbulletsに追加
def create_bullet():
    global bullet_timer, bullet_interval
    bullet_timer += 1
    if bullet_timer > bullet_interval:
        num_bullets = random.randint(1, 3)  # 一度に生成する弾の数
        for _ in range(num_bullets):
            bullet_x = random.randint(0, screen_width - bullet_width)
            bullet_y = 0
            bullets.append([bullet_x, bullet_y])
        bullet_interval = random.randint(min_bullet_interval, max_bullet_interval)
        bullet_timer = 0

# #プレイヤーと弾の衝突を判定
# def is_collision(player_x, player_y, bullet_x, bullet_y):
#     if player_x < bullet_x < player_x + player_width or bullet_x < player_x < bullet_x + bullet_width:
#         if player_y < bullet_y < player_y + player_height or bullet_y < player_y < bullet_y + bullet_height:
#             return True
#     return False

running = True
clock = pg.time.Clock()



move_key_dic = {
                pg.K_UP: (0, -5),
                pg.K_DOWN: (0, +5),
                pg.K_LEFT: (-5, 0),
                pg.K_RIGHT: (+5, 0),
}

### キャラクターの方向を管理する関数
def player_direction(img_path: str):
    player_img = pg.image.load(f"{img_path}")
    player_img = pg.transform.rotozoom(player_img, 0, 2.0)
    player_trans_img = pg.transform.flip(player_img, True, False)
    
    return {
        (0, 0): player_img,
        (0, -5): pg.transform.rotozoom(player_trans_img, 90, 1.0),
        (-5, 0): player_img,
        (+5, 0): player_trans_img,
        (+5, +5): pg.transform.rotozoom(player_trans_img, -45, 1.0),
        (0, +5): pg.transform.rotozoom(player_trans_img, -90, 1.0),
        (-5, +5): pg.transform.rotozoom(player_img, 45, 1.0),
        (-5, -5): pg.transform.rotozoom(player_img, 45, 1.0),
        (+5, -5): pg.transform.rotozoom(player_trans_img, 45, 1.0)
    }

### プレイヤーが壁抜けをしないようにする関数
def check_bound(obj_domain: pg.Rect):
    """"
    引数：こうかとんRectか、ばくだんRect
    戻値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    horizontal, vertical = True, True
    
    # 横方向判定
    if (obj_domain.left < 0) or (screen_width < obj_domain.right):
        horizontal = False
    
    # 縦方向判定
    if (obj_domain.top < 0) or (screen_height < obj_domain.bottom):
        vertical = False
    return horizontal, vertical


#プレイヤーのキー入力
#弾の生成、移動、描画、画面外に出た弾は削除
#プレイヤーと弾の衝突を検出、衝突した場合はゲームを終了。

# 🚩
"""
プレイキャラクター初期設定
"""
# player_img = pg.image.load("ex05/3.png")
# player_img = pg.transform.rotozoom(player_img, 0, 2.0)

player_direct_dic = player_direction("ex05/3.png") # 戻り値は辞書
player_img = player_direct_dic[(0, 0)] # 初期画像
player_rect = player_img.get_rect()
player_rect.center = (player_x, player_y) # 初期位置設定
# 🚩

while running:
    screen.fill(white) 

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pg.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    if keys[pg.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pg.K_DOWN] and player_y < screen_height - player_height:
        player_y += player_speed
    
    # 🚩
    # # プレイヤーの移動
    # for key, move_tpl in move_key_dic.items(): # dic={Press_KEY: (x, y)}
    #     if keys[key]:
    
    player_img = player_direct_dic[(player_x, player_y)]
    player_rect.move_ip(player_x, player_y)
    
    # プレイヤーはみ出し判定   
    if check_bound(player_rect) != (True, True):
        player_rect.move_ip(-player_x, -player_y)
        
    # 移動後の座標にプレイヤーを表示
    screen.blit(player_img, player_rect)
    # 🚩

    #生成
    create_bullet()

    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        pg.draw.rect(screen, black, [bullet[0], bullet[1], bullet_width, bullet_height])

        if bullet[1] > screen_height:
            bullets.remove(bullet)

        if (player_x < bullet[0] < player_x + player_width or
            bullet[0] < player_x < bullet[0] + bullet_width) and (
            player_y < bullet[1] < player_y + player_height or
            bullet[1] < player_y < bullet[1] + bullet_height):

            running = False  # ゲームオーバー
    

    # screen.blit(player_img, [player_x, player_y])
    # pg.draw.rect(screen, black, [player_x, player_y, player_width, player_height])
    pg.display.update()

    clock.tick(60)

pg.quit()