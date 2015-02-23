from pygame import *

screen = display.set_mode((800,600))
forestPic = image.load("images/forest.jpg") 
screen.blit(forestPic,(0,0))
running =True
while running:
    for e in event.get():
        if e.type == QUIT:
            running = False
   
    display.flip()

quit()
