from pygame import *

screen = display.set_mode((800,600))
kittyPic = image.load("images/kitty.png")
screen.fill((255,111,111))

running =True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()

    if mb[0]==1:
        screen.blit(kittyPic, (mx-175,my-172))
    display.flip()

quit()
