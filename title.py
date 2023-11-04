import pygame as pg
import sys
import threading


# pgの初期化
pg.init()

# 背景を動かすための関数
def move_background(bg_img: str):
    """
    bg_img: 背景画像のパス
    moving: global変数。Falseでこの関数の処理を停止する
    """
    clock  = pg.time.Clock()
    bg_trans_img = pg.transform.flip(bg_img, True, False)
    bg_lst = [bg_img, bg_trans_img]
    bg_lst = [bg_img, pg.transform.flip(bg_img, True, False)]*2
    
    bg_x = 0 # 毎秒移動する座標

    width = bg_img.get_width() # 背景画面の幅
    bg_flag = 0 # 背景を切り替えるためのフラグ変数
    while not in_game:
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        
        bg_x += 1
                
        if width <= bg_x: # 変化量が背景の大きさを越えた場合
            bg_x = 0
            bg_flag = 1 - bg_flag # これで交互にフラグを立てることが出来る
            
        screen.blit(bg_lst[bg_flag], [-bg_x, 0])
        
        # 背景画像の右側を描画（# width=1600を演算することで、切り替えた画像での原点を表現）
        screen.blit(bg_lst[1 - bg_flag], [width - bg_x, 0])    
        
        pg.display.update()
        clock.tick(1000)
    print("Finsh thread")
        

# 画面の幅と高さ
screen_width = 800
screen_height = 1000

# 画面の設定
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("DISPLAY_TITLE")

# タイトル画面の背景画像
bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
bg_img = pg.transform.rotozoom(bg_img, 0, 1.75)

# 背景を動かすスレッドを開始（無限ループのため、マルチスレッドを利用して並行処理）
bg_thread = threading.Thread(target=move_background, args=(bg_img,))
bg_thread.start()

# タイトル画面のフォントとテキスト
font = pg.font.Font(None, 46)
title_text = font.render("START", True, (0, 0, 0))


# 表示テキストの座標
"""
START :(39, 22) 例えば、get_widthならばオブジェクトの幅39を取得
x 座標: 361 (整数値) 400 - 39
y 座標: 488 (整数値) 500 - 22
"""
text_width = title_text.get_width() // 2
text_height = title_text.get_height() // 2
start_text_x = (screen_width // 2) - text_width
start_text_y = (screen_height // 2) - text_height

## 文字の背景長方形の描画
#透明を有効にしたsurface
scr =pg.Surface((text_width*2+80, text_height*2+40),flags=pg.SRCALPHA) # 長方形の大きさ # SRCALPHA=sorce alpha
# fillの第四引数に透過のα値を設定
scr.fill((255,255,255,150))

# ゲームループ
running = True
in_game = False

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # ゲーム中じゃないけど、背景を動かすmove_background()の処理を停止
            in_game = True
            # ウィンドウを閉じる
            running = False
        if event.type == pg.MOUSEBUTTONDOWN and not in_game:
            in_game = True
            
            # 別のpytonスクリプトを実行するexec()関数の利用
            exec(open("ex05/nobore_kokaton.py", encoding="utf8").read())

    # タイトル画面のオプションボタンを表示
    if not in_game:
        screen.blit(scr,(start_text_x-40, start_text_y-20)) # 文字背景の長方形を描画
        screen.blit(title_text, (start_text_x, start_text_y)) # startテキストボタンの描画

    pg.display.flip()

# pgの終了
pg.quit()
sys.exit()
