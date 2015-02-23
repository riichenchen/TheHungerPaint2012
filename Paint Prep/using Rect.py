from pygame import *
from random import *
from math import *
    
screen = display.set_mode((800,600))
pencilRect = Rect(20,80,40,40)
eraserRect = Rect(65,80,40,40)
arrow = [(200,200), (200,150), (190,150), (210,120), (230,150), (220,150), (220,200)]
font.init()
comicFont = font.SysFont("Comic Sans MS", 40)
sz=10
running =True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            mouse.set_visible(False)
        if e.type == MOUSEBUTTONUP:
            mouse.set_visible(True)
        if e.type == KEYDOWN:
            if e.key == K_LEFT:
                sz -= 1
            if e.key == K_RIGHT:
                sz += 1
                

    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()

    draw.rect(screen,(0,255,0),pencilRect,2)
    draw.rect(screen,(0,255,0),eraserRect,2)
    
    if pencilRect.collidepoint(mx,my):
        draw.rect(screen,(255,0,0),pencilRect,2)
    if eraserRect.collidepoint(mx,my):
        draw.rect(screen,(255,0,0),eraserRect,2)

    if mb[0]==1:
        txtPic = comicFont.render("Hello", True, (255,0,0))
        screen.blit(txtPic, (mx,my))
        #draw.circle(screen, (255,0,0), (mx,my), sz)
        #draw.polygon(screen,(255,0,0), arrow)

    display.flip()

font.quit()
del comicFont
quit()
