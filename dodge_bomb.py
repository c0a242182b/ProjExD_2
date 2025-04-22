import os
import random
import sys
import pygame as pg
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(5,0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
     """ 
     引数：こうかとんRectまたは爆弾Rect
     戻り値：判定結果タプル（横，縦）
     画面内ならTrue，画面外ならFalse
     """
     yoko, tate = True, True  # 横，縦方向用の変数
     # 横方向判定
     if rct.left < 0 or WIDTH < rct.right:  # 画面外だったら
         yoko = False
     # 縦方向判定
     if rct.top < 0 or HEIGHT < rct.bottom: # 画面外だったら
         tate = False
     return yoko, tate

def gameover(screen: pg.Surface) -> None:
    black = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(black,(0,0,0),(0,0,1300,1300),)
    black.set_alpha(100)
    screen.blit(black,(0,0))

    font=pg.font.Font(None,80)
    txt = font.render("Game Over" ,True,(255,255,255))
    screen.blit(txt,[400,300])

    img = pg.image.load("fig/8.png")
    screen.blit(img,[340,290])
    screen.blit(img,[720,290])
    
#def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
 
#     bb_accs = [a for a in range (1,11)]
#     bb_imgs = []
#     for r in range(1,11):
#         bb_img = pg.Surface((20*r, 20*r))
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
#         bb_img.set_colorkey((0,0,0))
#         bb_imgs.append(bb_img)
#     return bb_accs,bb_imgs   #途中


def main():
    tmr=0
    clock = pg.time.Clock()
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    bb_img = pg.Surface((20, 20)) 
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10) 
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5,+5
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        # こうかとんRectと爆弾Rectが重なっていたら
        if kk_rct.colliderect(bb_rct): 
            gameover(screen)
            
            pg.display.update()
            time.sleep(5)
            
            
            return
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        
        bb_accs = [a for a in range(1,11)]
        
        


        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # 画面外だったら
             kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右どちらかにはみ出ていたら
             vx *= -1
        if not tate:  # 上下どちらかにはみ出ていたら
             vy *= -1

        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
    


    
    
    clock = pg.time.Clock()
    tmr = 0

#    bb_accs , bb_imgs = init_bb_imgs()  #途中
#       avx = vx*bb_accs[min(tmr//500,9)]
#       bb_img = bb_imgs[min(tmr//500,9)]
#       bb_rct.move_ip(avx,vy)



    

        


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
