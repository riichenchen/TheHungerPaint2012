from pygame import *
    
screen = display.set_mode((800,600))

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

    if mb[0]==1:
        draw.circle(screen, (255,0,0), (mx,my), sz)

    display.flip()

font.quit()
del comicFont
quit()
