# keyboard.py
# Basic keyboard input. I use key.get_pressed() which just returns a list
# of boolean values for all of the keys. 

from pygame import *

screen = display.set_mode((800,600))

myClock = time.Clock()
x = 400
y = 300
running = True
while running:
    for evnt in event.get():                
        if evnt.type == QUIT:
            running = False

    keys = key.get_pressed()
    if keys[K_UP]:
            y -= 10
    if keys[K_DOWN]:
            y += 10
    if keys[K_RIGHT]:
            x += 10
    if keys[K_LEFT]:
            x -= 10
            
                
    screen.fill((0,0,0))
    draw.circle(screen, (255,0,0), (x,y), 20)
            
    display.flip()
    myClock.tick(60)                        
    
quit()
