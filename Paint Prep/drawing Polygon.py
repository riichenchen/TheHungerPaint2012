from pygame import *

    
screen = display.set_mode((800,600))
arrow = [(200,200), (200,150), (190,150), (210,120), (230,150), (220,150), (220,200)]

running =True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    draw.lines(screen, (255,0,0),True,arrow,2)
##    draw.polygon(screen,(255,0,0), arrow,2)

    display.flip()

quit()
