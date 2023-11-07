print("hello world")
import pygame
import random

pygame.init()

screen_width = 800
screen_height = 1000

white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("上に向かうゲーム")

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

#プレイヤーと弾の衝突を判定
def is_collision(player_x, player_y, bullet_x, bullet_y):
    if player_x < bullet_x < player_x + player_width or bullet_x < player_x < bullet_x + bullet_width:
        if player_y < bullet_y < player_y + player_height or bullet_y < player_y < bullet_y + bullet_height:
            return True
    return False

running = True
clock = pygame.time.Clock()

def check_bound(obj: pygame.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内か画面外かを判定し，真理値タプルを返す
    引数 obj：オブジェクト（爆弾，こうかとん，ビーム）SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj.left < 0 or screen_width < obj.right:  # 横方向のはみ出し判定
        yoko = False
    if obj.top < 0 or screen_height < obj.bottom:  # 縦方向のはみ出し判定
        tate = False
    return yoko, tate

def check_wall(obj: pygame.Rect):
    lst = [0 for i in range(4)]
    for i in range(len(lst)):
        if i == 0:
            if (obj.right>player_x>obj.left) and ((player_y+player_height>obj.top) and (player_y<obj.bottom)):
                lst[i] = 1
            else:
                lst[i] = 0
        elif i == 1:
            if (obj.left<player_x+player_width<obj.right) and ((player_y+player_height>obj.top) and (player_y<obj.bottom)):
                lst[i] = 1
            else:
                lst[i] = 0
        elif i == 2:
            if (obj.bottom>player_y>obj.top) and ((player_x+player_width>obj.left) and (player_x<obj.right)):
                lst[i] = 1
            else:
                lst[i] = 0
        elif i == 3:
            if (obj.top<player_y+player_height<obj.bottom) and ((player_x+player_width>obj.left) and (player_x<obj.right)):
                lst[i] = 1
            else:
                lst[i] = 0
            return lst

#障害物(壁)のクラス
class Wall:
    """
    障害物に関するクラス
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    def __init__(self):
        """
        引数に基づき壁Surfaceを作成する
        引数1 color: 壁の色
        """
        color = random.choice(__class__.colors)
        self.img = pygame.Surface((280,90))
        self.img.fill(color)
        x = random.randint(0, screen_width-280)
        y = random.randint(0, screen_height-90)
        pygame.draw.rect(self.img, color, (x,y,x+280,y+90))
        self.img.set_colorkey((0, 0, 0))
        self.rect = self.img.get_rect()
        self.rect.center = x+140, y+45

    def update(self, screen:pygame.Surface):
        """
        引数 screen 画面Surface
        """

        screen.blit(self.img, self.rect)
#プレイヤーのキー入力
#弾の生成、移動、描画、画面外に出た弾は削除
#プレイヤーと弾の衝突を検出、衝突した場合はゲームを終了。

#壁のインスタンスを複数つくる
wall_num = 3
lst = [0 for i in range(wall_num)]
walls = [Wall() for i in range(wall_num)]
while running:
    screen.fill(white) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #複数の壁を表示させる
    for i, wall in enumerate(walls):
        lst[i] = check_wall(wall.rect)
        wall.update(screen)
        

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        for data in lst:
            if data[0] == 1:
                player_x += player_speed+0.5
                break
        else:
            player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        for data in lst:
            if data[1] == 1:
                player_x-=player_speed+0.5
                break
        else:
            player_x += player_speed
    if keys[pygame.K_UP] and player_y > 0:
        for data in lst:
            if data[2] == 1:
                player_y += player_speed+0.5
                break
        else:
            player_y -= player_speed
    if keys[pygame.K_DOWN] and player_y < screen_height - player_height:
        for data in lst:
            if data[3] == 1:
                player_y -= player_speed+0.5
                break
        else:
            player_y += player_speed

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
    

    pygame.draw.rect(screen, black, (player_x, player_y, player_width, player_height))
    pygame.display.update()

    clock.tick(60)

pygame.quit()