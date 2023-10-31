print("hello world")
import pygame as pg
import random
import time

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

# プレイキャラクター画像を取得
explosion_ef = pg.image.load("ex05/explosion.gif")
chara = pg.image.load("ex05/3.png")


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


#プレイヤーのキー入力
#弾の生成、移動、描画、画面外に出た弾は削除
#プレイヤーと弾の衝突を検出、衝突した場合はゲームを終了。

while running:
    screen.fill(white) # 背景色を設定
    # exps = Explosion()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # プレイヤーの移動処理
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pg.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    if keys[pg.K_UP] and player_y > 0:
        player_y -= player_speed
    if keys[pg.K_DOWN] and player_y < screen_height - player_height:
        player_y += player_speed

    # 敵（bullet）の生成
    create_bullet()
    # exps = pg.sprite.Group()
    
    # bullets = 二次元リスト
    # bullet  = 敵のx, y座標 を含むリスト
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        
        # 生成した敵の座標設定
        pg.draw.rect(screen, black, [bullet[0], bullet[1], bullet_width, bullet_height])
        
        # 画面外のbullet（敵）を削除するための処理
        if bullet[1] > screen_height:
            bullets.remove(bullet)

        # bulletとプレイヤーの衝突判定
        if (player_x < bullet[0] < player_x + player_width or
            bullet[0] < player_x < bullet[0] + bullet_width) and (
            player_y < bullet[1] < player_y + player_height or
            bullet[1] < player_y < bullet[1] + bullet_height):

            # 衝突時にプレイヤーが爆発するようにする
            screen.blit(explosion_ef, [player_x, player_y])
            pg.display.update()
            time.sleep(0.5) # 死亡エフェクトを目立たせるため、少しだけ停止
            running = False  # ゲームオーバー
    
    # プレイヤーの生成
    pg.draw.rect(screen, black, [player_x, player_y, player_width, player_height])
    pg.display.update()

    clock.tick(60)

pg.quit()