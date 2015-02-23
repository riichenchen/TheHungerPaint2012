from pygame import *
from random import *

    
screen = display.set_mode((800,600))
wheel = image.load("pallet.jpg")
screen.blit(wheel,(0,0))
clr = (255,0,255)
running =True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()

    if mb[0]==1:
        draw.circle(screen,clr,(mx,my),5)
    if mb[2]==1:
        clr = screen.get_at((mx,my))
        draw.rect(screen,clr,(0,0,20,20))
    display.flip()

quit()
