import random
import sys
import time

import pygame as pg


WIDTH = 1600  # ゲームウィンドウの幅
HEIGHT = 900  # ゲームウィンドウの高さ
NUM_OF_BOMBS = 2 # 爆弾の数


def check_bound(obj_rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数：こうかとん，または，爆弾SurfaceのRect
    戻り値：横方向，縦方向のはみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


class Bird:
    """
    ゲームキャラクター（こうかとん）に関するクラス
    """
    delta = {  # 押下キーと移動量の辞書
        pg.K_UP: (0, -5),
        pg.K_DOWN: (0, +5),
        pg.K_LEFT: (-5, 0),
        pg.K_RIGHT: (+5, 0),
    }

    def __init__(self, num: int, xy: tuple[int, int]):
        """
        こうかとん画像Surfaceを生成する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 xy：こうかとん画像の位置座標タプル
        """
        img0 = pg.transform.rotozoom(pg.image.load(f"ex03/fig/{num}.png"), 0, 2.0)
        img = pg.transform.flip(img0, True, False)  # デフォルトのこうかとん（右向き）
        self.imgs = {  # 0度から反時計回りに定義
            (+5, 0): img,  # 右
            (+5, -5): pg.transform.rotozoom(img, 45, 1.0),  # 右上
            (0, -5): pg.transform.rotozoom(img, 90, 1.0),  # 上
            (-5, -5): pg.transform.rotozoom(img0, -45, 1.0),  # 左上
            (-5, 0): img0,  # 左
            (-5, +5): pg.transform.rotozoom(img0, 45, 1.0),  # 左下
            (0, +5): pg.transform.rotozoom(img, -90, 1.0),  # 下
            (+5, +5): pg.transform.rotozoom(img, -45, 1.0),  # 右下
        }
        self.img = self.imgs[(+5, 0)]
        self.rct = self.img.get_rect()
        self.rct.center = xy

    def change_img(self, num: int, screen: pg.Surface):
        """
        こうかとん画像を切り替え，画面に転送する
        引数1 num：こうかとん画像ファイル名の番号
        引数2 screen：画面Surface
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"ex03/fig/{num}.png"), 0, 2.0)
        screen.blit(self.img, self.rct)

    def update(self, key_lst: list[bool], screen: pg.Surface):
        """
        押下キーに応じてこうかとんを移動させる
        引数1 key_lst：押下キーの真理値リスト
        引数2 screen：画面Surface
        """
        sum_mv = [0, 0]
        for k, mv in __class__.delta.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        self.rct.move_ip(sum_mv)
        if check_bound(self.rct) != (True, True):
            self.rct.move_ip(-sum_mv[0], -sum_mv[1])
        if not (sum_mv[0] == 0 and sum_mv[1] == 0):
            self.img = self.imgs[tuple(sum_mv)]
        screen.blit(self.img, self.rct)


class Beam:
    def __init__(self, bird: Bird):
        """
        ビーム画像Surfaceを生成する
        引数 bird：こうかとんインスタンス（Birdクラスのインスタンス）
        """
        self.img = pg.transform.rotozoom(pg.image.load(f"ex03/fig/beam.png"), 0, 2.0) # ビームの大きさを二倍
        self.rct = self.img.get_rect()
        self.rct.left = bird.rct.right  # こうかとんの右横座標
        self.rct.centery = bird.rct.centery  # こうかとんの中心縦座標
        self.vx, self.vy = +5, 0

    def update(self, screen: pg.Surface):
        """
        ビームを速度vxにしたがって移動させる
        引数 screen：画面Surface
        """
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)        


class Bomb:
    """
    爆弾に関するクラス
    """
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
    directions = [-5, +5]
    
    def __init__(self):
        """
        ランダムな色，サイズの爆弾円Surfaceを生成する
        """
        rad = random.randint(10, 50)  # 半径をランダムに設定
        color = random.choice(__class__.colors)
        self.img = pg.Surface((2*rad, 2*rad))
        pg.draw.circle(self.img, color, (rad, rad), rad)
        self.img.set_colorkey((0, 0, 0))
        self.rct = self.img.get_rect()
        self.rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
        self.vx = random.choice(__class__.directions)
        self.vy = random.choice(__class__.directions)

    def update(self, screen: pg.Surface):
        """
        爆弾を速度ベクトルself.vx, self.vyに基づき移動させる
        引数 screen：画面Surface
        """
        yoko, tate = check_bound(self.rct)
        if not yoko:
            self.vx *= -1
        if not tate:
            self.vy *= -1
        self.rct.move_ip(self.vx, self.vy)
        screen.blit(self.img, self.rct)
        

class Explosion:
    """"
    爆発に関するクラス
    """
    def __init__(self, bomb: Bomb, life: int):
        """
        ex03/fig/explosion.gifと上下左右にflip したものを画像リストに格納
        爆発した爆弾のrct.center に基づき，生成場所を決定
        表示時間（爆発時間）life を設定
        """
        self.bomb = bomb
        self.ep_img = pg.image.load("ex03/fig/explosion.gif")
        self.ep_lst = [
                self.ep_img,
                pg.transform.flip(self.ep_img, True, True),
                pg.transform.flip(self.ep_img, True, False),
                pg.transform.flip(self.ep_img, False, True),
                pg.transform.flip(self.ep_img, False, False)
        ]
        self.genloc = self.ep_img.get_rect() # 爆発した爆弾の生成場所を決定
        self.genloc.center = bomb.rct.center
        self.life = life # 爆発表示時間の設定
        
    def update(self, screen: pg.Surface):
        """"
        •爆発経過時間life を１減算
        •爆発経過時間life の値に応じて，画像リストを交互に切り替えて爆発を演出
        """
        self.life -= 1
        screen.blit(self.ep_img, self.genloc)


def main():
    pg.display.set_caption("たたかえ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))    
    bg_img = pg.image.load("ex03/fig/pg_bg.jpg")
    bird = Bird(3, (900, 400))
    bombs = [Bomb() for _ in range(NUM_OF_BOMBS)]
    beam = None
    explosion_lst = list()

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                # キーが押されたら，かつ，キーの種類がスペースキーだったら
                beam = Beam(bird)# Beamイニシャライザの中のことが行われる

        
        screen.blit(bg_img, [0, 0])
        
        for bomb in bombs:
            if bird.rct.colliderect(bomb.rct):
                # ゲームオーバー時に，こうかとん画像を切り替え，1秒間表示させる
                bird.change_img(8, screen)
                pg.display.update()
                time.sleep(1)
                return
        
        for i, bomb in enumerate(bombs):
            if beam is not None:
                if beam.rct.colliderect(bomb.rct):  # ビームと爆弾の衝突判定
                    # 撃墜＝Noneにする
                    beam = None
                    bombs[i] = None
                    
                    explosion_lst.append(Explosion(bomb, 100))
                    # Explosion.update()
                        
                    bird.change_img(6, screen) # 撃墜したら喜ぶ画像に変更
                    pg.display.update()
                    
        bombs = [bomb for bomb in bombs if bomb is not None]
        explosions = [epl for epl in explosion_lst if epl.life > 0]

        key_lst = pg.key.get_pressed()
        bird.update(key_lst, screen)
        # for bomb in bombs:
            # bomb.update(screen)
        # if beam is not None:
        #     beam.update(screen)
        # for epl in explosions:
        #     epl.update(screen)    
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()