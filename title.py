import pygame as pg
import sys
import threading


# pgの初期化
pg.init()

class Canvas:
    width = 600
    height = 400
    
    def __init__(self, screen, width: int, height: int, chara_idx=0):
        """
        引数1 main_screen: 基になるメインのスクリーン\n
        引数2 width: 新しく表示されるウィンドウもどきの幅\n
        引数3 height: 新しく表示されるウィンドウもどきの高さ\n
        """
        self.screen = screen
        self.width = width
        self.height = height
        self.chara_idx = chara_idx
        self.rect_x = 0
        self.rect_y = 0
        
        self.load_chara_images() # 画像の読み込みを初期化

    # 背景用の白い長方形を作成する関数
    def background_rectangle(self, display_only=False):
        pg.draw.rect(self.screen, 
                     (255, 255, 255), 
                     (self.rect_x, self.rect_y, self.width, self.height)
                     )
        # その他の処理はせず、白い背景を表示させたいだけの時の処理
        if display_only:
            pg.display.flip()
    
    # closeとテキストを表示させる関数
    def close_text(self, received_return=True):
        """
        引数1 received_return: Falseを引数として指定すれば、座標を戻り値を取り出せる
        """
        font = pg.font.Font(None, 46)
        close_text = font.render("CLOSE", True, (0, 0, 0))
        close_w = close_text.get_width() // 2
        close_h = close_text.get_height()
        close_x = __class__.width//2 + close_w
        close_y = 900 
        
        # blitするかreturnするかの処理
        if received_return:
            self.screen.blit(close_text, (close_x, close_y))
        else:
            return close_w, close_h, close_x, close_y

        
    # キャラクター画像の情報を読み込む関数
    def load_chara_images(self):
        self.chara_img_lst = [] # リストの初期化
        img_size_space = 0
        playable_lst = ["ex05/3.png", "ex05/koba.png", "ex05/bluebird_enjou.png"] # プレイキャラクター
        for i, img_path in enumerate(playable_lst):
            img = pg.image.load(img_path)
            player_img = pg.transform.scale(img, (120, 120))
            player_rect = player_img.get_rect()
            
            # 選択キャラクター画像配置の設定
            if i == 0:
                img_size_space += 120
                
            else:
                img_size_space += 120 + 40
            player_rect.center = (img_size_space, 100) # (x, y)
            self.chara_img_lst.append((player_img, player_rect)) # 画像とそのrect情報をタプルでリストに追加していく
    
    # キャラクターの画像を描画する関数
    def draw_characters(self):
        for player_img, player_rect in self.chara_img_lst:
            self.screen.blit(player_img, player_rect)
    
    # 描画等の処理を行う
    def main(self, display_only=False):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return self.chara_idx
                
                if event.type == pg.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    # print(f"x: {mouse_x}, y: {mouse_y}")
                    close_w, close_h, close_x, close_y = self.close_text(False) # Falseで値を取り出せる
                    
                    if not display_only:
                        """プレイアブルキャラクターの変更処理"""
                        # load_chara_images()のplayer_rectを受け取り、mouseとジャッジ
                        if 60 <= mouse_x <= 60 + 120 and\
                            30 <= mouse_y <= 30 + 120:
                                # print("❓")
                                # print(f"x: {mouse_x}, y: {mouse_y}")
                                self.chara_idx = 0
                                return self.chara_idx
                        elif (60 + 120) + 40 <= mouse_x <= 220 + 120 and\
                            30 <= mouse_y <= 30 + 120:
                                self.chara_idx = 1
                                return self.chara_idx
                        elif (220 + 120) + 40 <= mouse_x <= 380 + 120 and\
                            30 <= mouse_y <= 30 + 120:
                                self.chara_idx = 2
                                return self.chara_idx
                            
                    
                    ## closeテキストをクリックしたらキャラクター画面を閉じる
                    if close_x <= mouse_x <= close_x*1.15 + close_w and\
                        close_y <= mouse_y <= close_y + close_h:
                        """closeテキストのマウスにおけるクリック判定"""
                        return self.chara_idx
                        
                    # # クリックした位置が長方形内であれば、長方形を消す（座標closeにしたかったけど面倒くさいからあとで）
                    # elif self.rect_x <= mouse_x <= self.rect_x + self.width and self.rect_y <= mouse_y <=self. rect_y + self.height:
                    #     return self.chara_idx
                        
            self.screen.fill((255, 255, 255)) # 暗転を防ぐ？
            self.background_rectangle()  # 白い長方形を描画
            # 白い長方形背景を描画させたいだけのときの処理
            if display_only:
                self.close_text()
                pg.display.flip()
            else:
                self.draw_characters() # 白い長方形の上にキャラクターを描画
                self.close_text() # 背景を動かすとなぜか点滅してしまうのでコメントアウト推奨
                pg.display.flip()
            

# 背景を動かすための関数
# ❗たまに画面点滅する不具合アリ❗
def move_background(bg_img):
    """
    bg_img: 背景画像のパス
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
    
        
# 白いボタンを作成する関数      
# 引数に入れていないのになんかscreen_width使えた
def option_button(text, diff_num=0, div_num=7):
    # 表示テキストの座標
    """
    引数： text 幅高さを持つオブジェクト\n
    戻り値: text_width, text_height, text_x, text_y\n
    """
    text_width = (text.get_width() // 2) * 2 + 80
    text_height = (text.get_height() // 2) * 2 + 40
    text_x = (screen_width) - text_width - (80) # (80)は微調整分
    text_y = (screen_height // 2) - text_height + (244)

    ## 文字の背景長方形の描画
    #透明を有効にしたsurface
    scr =pg.Surface((text_width, text_height),flags=pg.SRCALPHA) # 長方形の大きさ # SRCALPHA=sorce alpha
    # fillの第四引数に透過のα値を設定
    scr.fill((255,255,255,150))
    
    screen.blit(scr,(text_x - diff_num, text_y)) # 文字背景の長方形を描画
    screen.blit(text, ((text_x - diff_num) + (text_width // div_num), text_y + text_height // 3)) # startテキストボタンの描画
    return text_width, text_height, text_x, text_y

# タイトル文字を作成する関数
def title(screen, screen_width: int, screen_height: int):
    font = pg.font.Font(None, 106)
    title_text = font.render("RISE! KOKATON!!", True, (0, 0, 0))
    text_width =  title_text.get_width() // 2
    # text_height = title_text.get_height()
    title_text_x = (screen_width // 2) - text_width
    title_text_y = (screen_height//4)
    screen.blit(title_text, (title_text_x, title_text_y))


# 画面の幅と高さ
screen_width = 800
screen_height = 1000

# 画面の設定
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("DISPLAY_TITLE")

# タイトル画面の背景画像
bg_img = pg.image.load("ex05/fig/pg_bg.jpg")
bg_img = pg.transform.rotozoom(bg_img, 0, 1.75)

# # 背景を動かすスレッドを開始（無限ループのため、マルチスレッドを利用して並行処理）
# bg_thread = threading.Thread(target=move_background, args=(bg_img,))
# bg_thread.start()
    
    
# タイトル画面のフォントとテキスト
font = pg.font.Font(None, 46)
start_text = font.render("START", True, (0, 0, 0))
select_cahara_text = font.render("CHARACTER", True, (0, 0, 0))
level_text = font.render("LEVEL", True, (0, 0, 0))

### 表示テキストの座標
"""
START :(39, 22) 例えば、get_widthならばオブジェクトの幅39を取得
x 座標: 361 (整数値) 400 - 39
y 座標: 488 (整数値) 500 - 22
"""
text_width = start_text.get_width() // 2
text_height = start_text.get_height() // 2
start_text_x = (screen_width // 2) - text_width
start_text_y = (screen_height // 2) - text_height

## 文字の背景長方形の描画
#透明を有効にしたsurface
scr =pg.Surface((text_width*2+80, text_height*2+40), flags=pg.SRCALPHA) # 長方形の大きさ # SRCALPHA=sorce alpha
# fillの第四引数に透過のα値を設定
scr.fill((255,255,255,150))
            

# ゲームループ
running = True
in_game = False # 本編ゲームに入ったら（タイトル画面が切り替わるなら）Trueになる
chara_idx = 0 # キャラクター選択情報を保存するための値
chara_canvas = Canvas(screen, screen_width, screen_height, chara_idx)
level_canvas = Canvas(screen, screen_width, screen_height)
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            # ゲーム中じゃないけど、背景を動かすmove_background()の処理を停止
            in_game = True
            # ウィンドウを閉じる
            running = False
            
        ### マウスでクリックされたら
        if event.type == pg.MOUSEBUTTONDOWN and not in_game:
            # マウスクリック時の座標を取得
            mouse_x, mouse_y = pg.mouse.get_pos()
            
            """STARTボタンクリックの当たり判定"""
            # クリックされたテキストごとに処理を分ける
            # -40や-20は先の長方形の大きさを微調整した際の量
            if (start_text_x - 40) <= ( mouse_x ) <= (start_text_x + text_width * 2 + 40) and\
                (start_text_y -20) <= ( mouse_y ) <= (start_text_y + text_height * 2 + 20):
                # "START"テキストがクリックされた時の処理
                in_game = True
            
                # 別のpytonスクリプトを実行するexec()関数の利用
                exec(open("ex05/temp.py", encoding="utf8").read())
            
            """CHARACTERボタンクリックの当たり判定"""
            # キャラクター選択のための新しいウィンドウを表示させる
            if (chara_x) <= ( mouse_x ) <= (chara_x + cahra_w) and\
                (chara_y) <= ( mouse_y ) <= (chara_y + chara_h):
                # キャラクター選択用ウィンドウのインスタンスを作成
                chara_idx = chara_canvas.main() # 選んだキャラクターが戻り値で返ってくる。この値はゲームのスクリプトにも引き継がれる
            
            print(f"x: {lev_x}, y: {lev_y}, mouse_x: {mouse_x}, mouse_y: {mouse_y}")
            """LEVELボタンの当たり判定"""
            # 難易度設定を行うボタン
            # if (lev_x) <= ( mouse_x ) <= (lev_x + lev_w) and\
            #     (lev_y) <= ( mouse_y ) <= (lev_y + lev_h):
            # なんかうまくいかなかったので直接指定
            if (190) <= ( mouse_x ) <= (190 + lev_w) and\
                (675) <= ( mouse_y ) <= (675 + lev_h):
                
                # print("level")
                # 難易度設定処理
                level_canvas.main(True) # Trueで白い背景のみ描画
                


    # タイトル画面のオプションボタンを表示
    if not in_game:
        screen.blit(bg_img, (0, 0)) # 静止背景を描画
        cahra_w, chara_h, chara_x, chara_y = option_button(select_cahara_text) # CHARACTERボタンを作成し、戻り値を取得
        lev_w, lev_h, lev_x, lev_y = option_button(level_text, 350, 4) # levelボタン作成・大きさと座標を受け取る
        title(screen, screen_width, screen_height) # なんか関数側も削除すれば、引数なしでも呼び出せる
        screen.blit(scr,(start_text_x-40, start_text_y-20)) # 文字背景の長方形を描画
        screen.blit(start_text, (start_text_x, start_text_y)) # startテキストボタンの描画
        
        

    pg.display.flip()

# pgの終了
pg.quit()
sys.exit()
