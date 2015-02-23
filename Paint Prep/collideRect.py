from pygame import *
from random import *
from math import *
    
screen = display.set_mode((800,600))
pencilRect = Rect(20,80,40,40)
eraserRect = Rect(65,80,40,40)
running =True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False

    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()

    draw.rect(screen,(0,255,0),pencilRect,2)
    draw.rect(screen,(0,255,0),eraserRect,2)
    
    if pencilRect.collidepoint(mx,my):
        draw.rect(screen,(255,0,0),pencilRect,2)
    if eraserRect.collidepoint(mx,my):
        draw.rect(screen,(255,0,0),eraserRect,2)
        
    display.flip()

quit()
