print("hello world")
import pygame
import random

pygame.init()

screen_width = 800
screen_height = 1000

white = (255, 255, 255)
black = [0,0,0]
#bird = pygame.image.load("ex05/fig/3.png")

screen = pygame.display.set_mode((screen_width, screen_height))
#bg_img = pygame.image.load("ex05/fig/pg_bg.jpg")
pygame.display.set_caption("上に向かうゲーム")

#プレイヤーのサイズと初期位置、移動速度を設定
player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 30
player_speed = 10

#プレイヤーの進んだ距離を記録する変数
r = 0

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

#プレイヤーと弾の衝突を判定
def is_collision(player_x, player_y, bullet_x, bullet_y):
    if player_x < bullet_x < player_x + player_width or bullet_x < player_x < bullet_x + bullet_width:
        if player_y < bullet_y < player_y + player_height or bullet_y < player_y < bullet_y + bullet_height:
            return True
    return False

running = True
clock = pygame.time.Clock()

tmr = 0
font = pygame.font.SysFont("hgp創英角ﾎﾟｯﾌﾟ体", 30)
#プレイヤーのキー入力
#弾の生成、移動、描画、画面外に出た弾は削除
#プレイヤーと弾の衝突を検出、衝突した場合はゲームを終了。

while running:
    screen.fill(white)
    txt = font.render(f"Time:{int(tmr/60):03}", True, (0, 0, 255))
    screen.blit(txt, [600, 10])
    #screen.blit(bg_img, [0, 0])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if r <= 2000:
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
            player_x += player_speed
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= player_speed
            r += 20
        if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
            player_y += player_speed
            r -= 10

        #生成
        create_bullet()

        for bullet in bullets[:]:
            bullet[1] += bullet_speed
            pygame.draw.rect(screen, black, [bullet[0], bullet[1], bullet_width, bullet_height])

            if bullet[1] > screen_height:
                bullets.remove(bullet)

            if (player_x < bullet[0] < player_x + player_width or
                bullet[0] < player_x < bullet[0] + bullet_width) and (
                player_y < bullet[1] < player_y + player_height or
                bullet[1] < player_y < bullet[1] + bullet_height):

                running = False  # ゲームオーバー
    
    if r >= 2000:
        r = 20000
        txt2 = font.render("game clear", True, (255, 0, 255))
        screen.blit(txt2, [300, 500])
    else:
        txt3 = font.render(f"ゴールまで{2000-r:03}m", True, (255, 0, 255))
        screen.blit(txt3, [0, 10])
    
    pygame.draw.rect(screen, black, [player_x, player_y, player_width, player_height])
    pygame.display.update()
    if r <= 2000:
        tmr += 1
    clock.tick(60)

pygame.quit()