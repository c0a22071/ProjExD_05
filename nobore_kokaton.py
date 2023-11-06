print("hello world")
import pygame as pg
import random

pg.init()

screen_width = 800
screen_height = 1000

white = (255, 255, 255)
black = (0, 0, 0)

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Drink It Down")

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

# 闇の画像をロード
dark_size = 1.5
d_img = pg.image.load("ex05/darkness.jpeg")
d_img = pg.transform.rotozoom(d_img, 0, dark_size)
d_img_top = pg.transform.flip(d_img, False, True)


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

#プレイヤーと弾の衝突を判定
def is_collision(player_x, player_y, bullet_x, bullet_y):
    if player_x < bullet_x < player_x + player_width or bullet_x < player_x < bullet_x + bullet_width:
        if player_y < bullet_y < player_y + player_height or bullet_y < player_y < bullet_y + bullet_height:
            return True
    return False

running = True
clock = pg.time.Clock()
dark_y = screen_height # 闇の初期位置
dark_speed = 1 # 闇の浸食する速さ
scroll_area = 2/5 # スクロールを開始する範囲（一番上から）

#プレイヤーのキー入力
#弾の生成、移動、描画、画面外に出た弾は削除
#プレイヤーと弾の衝突を検出、衝突した場合はゲームを終了。

while running:
    screen.fill(white) 

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # 闇を表示
    screen.blit(d_img_top, [0, dark_y])
    screen.blit(d_img, [0, dark_y + (340 * dark_size)])
    dark_y -= dark_speed

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pg.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    if keys[pg.K_UP] and player_y > 0:
        player_y -= player_speed
        if player_y < (screen_height * scroll_area):
            dark_y += player_speed
    if keys[pg.K_DOWN] and player_y < screen_height - player_height:
        player_y += player_speed

    #生成
    create_bullet()

    # 闇が完全に画面を覆いつくしたらゲームオーバー
    if dark_y < 0:
        running = False

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
    

    pg.draw.rect(screen, black, [player_x, player_y, player_width, player_height])
    pg.display.update()

    clock.tick(60)

pg.quit()