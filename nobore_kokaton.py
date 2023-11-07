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

# 背景画像の読み込み
bg_img = pg.image.load("ex05/fig/kumo38.png")
rotated_bg_img = pg.transform.flip(bg_img, False, True)

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

running = True
clock = pg.time.Clock()
dark_y = screen_height # 闇の初期位置
dark_speed = 1 # 闇の浸食する速さ
scroll_area = 2/5 # スクロールを開始する範囲（一番上から）

# 画像をスクロールさせる為に必要な変数ども
bg_height = 1080
tmr = 0
bg_y = 0
bg_y_2 = bg_height
scroll_area = 2/5 # スクロールを開始する範囲（一番上から）

move_key_dic = {
                pg.K_UP: (0, -5),
                pg.K_DOWN: (0, +5),
                pg.K_LEFT: (-5, 0),
                pg.K_RIGHT: (+5, 0),
}

### キャラクターの方向を管理する関数
def player_direction(player_img):
    """
    引数1 player_img: 画像データ
    """
    # player_img = pg.image.load(f"{img_path}")
    player_img = pg.transform.rotozoom(player_img, 0, 2.0)
    player_trans_img = pg.transform.flip(player_img, True, False)
    
    return {
        (0, 0): player_img, # 初期位置（左)
        (+5, 0): player_trans_img,  # 右
        (+5, -5): pg.transform.rotozoom(player_trans_img, 45, 1.0),  # 右上
        (0, -5): pg.transform.rotozoom(player_img, -90, 1.0),  # 上 # 最初はplayer_trans_img, 90
        (-5, -5): pg.transform.rotozoom(player_img, -45, 1.0),  # 左上
        (-5, 0): player_img,  # 左
        (-5, +5): pg.transform.rotozoom(player_img, 45, 1.0),  # 左下
        (0, +5): pg.transform.rotozoom(player_trans_img, -90, 1.0),  # 下
        (+5, +5): pg.transform.rotozoom(player_trans_img, -45, 1.0),  # 右下
    }


#プレイヤーのキー入力
#弾の生成、移動、描画、画面外に出た弾は削除
#プレイヤーと弾の衝突を検出、衝突した場合はゲームを終了。

# 🚩
### """プレイキャラクター初期設定"""
# global playable_path # 値はtitle.pyで更新される
global chara_idx # 値はtitle.pyで更新される
playable_lst = ["ex05/3.png", "ex05/koba.png", "ex05/bluebird_enjou.png"]
player_img = pg.image.load(playable_lst[chara_idx])
player_img = pg.transform.scale(player_img, (48, 48)) # 48*48にリサイズ
player_direction_dic = player_direction(player_img) # プレイヤーの顔の向きを決める辞書。引数には画像パスを指定
player_img = player_direction_dic[(0, 0)] # 辞書のバリューにある初期の画像を受け取る
player_rect = player_img.get_rect()
player_rect.topleft = (0, 0)
player_speed = 5 # 移動速度
player_x = 365 # 初期x座標
player_y = 890 # 初期y座標
sum_move = [0, 0]
# 🚩

while running:
    screen.fill(white) # 背景色を設定
    # exps = Explosion()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
            
    # 背景が下端に到達したら反対側にやる
    if bg_y >= bg_height:
        bg_y = -bg_height
    if bg_y_2 >= bg_height:
        bg_y_2 = -bg_height

    # 闇を表示
    screen.blit(d_img_top, [0, dark_y])
    screen.blit(d_img, [0, dark_y + (340 * dark_size)])
    dark_y -= dark_speed

    # 背景の表示
    screen.blit(bg_img, [0, bg_y])
    screen.blit(rotated_bg_img, [0, bg_y_2])
    
    # 背景の座標を更新
    tmr += 1
            

    keys = pg.key.get_pressed()

    if keys[pg.K_LEFT] and player_x > 0:
        player_x -= player_speed

    if keys[pg.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed

    if keys[pg.K_UP]:
        # if player_y > 0:
        #     player_y -= player_speed

        # 画面上部4分の1範囲にいるときはスクロールする
        if player_y < (screen_height * scroll_area):
            bg_y += player_speed
            bg_y_2 += player_speed
            dark_y += player_speed
        else:
            player_y -= player_speed

    if keys[pg.K_DOWN]:
        if player_y < screen_height - player_height:
            player_y += player_speed
    
    
        
    # 🚩
    """
    プレイヤーの移動
    sum_moveは辞書のキーであるため、常にmax・min ±5の範囲にある
    """
    # 辞書のバリューは±5しかないので、keyErrorが起きないよう演算する処理
    for key, move_tpl in move_key_dic.items():
        if keys[key]:
            sum_move[0] += move_tpl[0]
            sum_move[1] += move_tpl[1]  

    """
    プレイヤーのはみ出し判定
    """
    # 移動範囲の制限を追加（プレイヤーが壁を突き抜けないようにする処理）
    # 以下の5と100はどんなに座標が小さくなってもプレイヤーの座標が5と700になるようにするためのもの
    player_x = max(5, min(player_x, screen_width - 100))
    player_y = max(5, min(player_y, screen_height - 100))

    """
    プレイヤーの顔の向きを選択
    """
    # 移動値±5により、KeyErrorとなるのを防ぐための処理
    # sum_moveを加算することで、顔の向きを更新保持する処理
    # (10, y)のときを想定
    if (sum_move[0] > 5):
        sum_move = [0, 0]
        for key, move_tpl in move_key_dic.items():
            if keys[key]:
                sum_move[0] += move_tpl[0]
                sum_move[1] += move_tpl[1] 
    # (-10, y)のときを想定
    if (sum_move[0]  < -5):
        sum_move = [0, 0]
        for key, move_tpl in move_key_dic.items():
            if keys[key]:
                sum_move[0] += move_tpl[0]
                sum_move[1] += move_tpl[1] 
    # (x, 10)のときを想定
    if (sum_move[1] > 5):
        sum_move = [0, 0]
        for key, move_tpl in move_key_dic.items():
            if keys[key]:
                sum_move[0] += move_tpl[0]
                sum_move[1] += move_tpl[1] 
    # (x, -10)のときを想定
    if (sum_move[1] < -5):
        sum_move = [0, 0]
        for key, move_tpl in move_key_dic.items():
            if keys[key]:
                sum_move[0] += move_tpl[0]
                sum_move[1] += move_tpl[1] 
    
    # ±5の方向のタプルの辞書キーに応じて、顔の方向の画像を受け取る
    player_img = player_direction_dic[tuple(sum_move)]

    # プレイヤーの位置を直接設定
    player_rect.topleft = (player_x, player_y)
        
    # 移動後の座標にプレイヤーを表示
    screen.blit(player_img, player_rect)
    # 🚩

    # 敵（bullet）の生成
    create_bullet()
    # exps = pg.sprite.Group()
    
    # 闇が完全に画面を覆いつくしたらゲームオーバー
    if dark_y < 0:
        running = False
    
    # bullets = 二次元リスト
    # bullet  = 敵のx, y座標 を含むリスト
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        pg.draw.rect(screen, black, [bullet[0], bullet[1], bullet_width, bullet_height])

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
    

    # screen.blit(player_img, [player_x, player_y])
    # pg.draw.rect(screen, black, [player_x, player_y, player_width, player_height])
    pg.display.update()

    clock.tick(60)

# pg.quit()