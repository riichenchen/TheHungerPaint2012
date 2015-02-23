from pygame import *
    
screen = display.set_mode((800,600))

start = 0,0
size = 10
running =True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
           if e.button == 1:
               start = e.pos
           if e.button == 4:
               size += 1
           if e.button == 5:
               size -= 1
            
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()

    if mb[0]==1:
        screen.fill((0,0,0))
        draw.line(screen, (255,0,0), start,(mx,my), size)

    display.flip()

quit()
