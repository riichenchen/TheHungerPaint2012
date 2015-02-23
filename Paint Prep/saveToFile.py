from pygame import *
    
screen = display.set_mode((1200,675))

canvasRect = Rect(100,50,900,575)
running =True
screen.fill((255,255,255))
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 2:
                image.save(screen.subsurface(canvasRect),"myPic.png")
    
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()

    draw.rect(screen,(0,0,0), canvasRect,2)
    if mb[0]==1:
        draw.circle(screen, (0,0,0), (mx,my), 3)

    display.flip()

quit()
