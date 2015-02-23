from pygame import *
from random import *
    
screen = display.set_mode((1000,600))

font.init()
comicFont = font.SysFont("Comic Sans MS", 20)
quotes = ["The road to success is always under construction.",
        "Worst excuse for not turning in homework: I couldn't find anyone to copy it from.",
        "A computer once beat me at chess, but it was no match for me at kick boxing.",
        "I am so clever that sometimes I don't understand a single word of what I am saying.",
        "Never go to a doctor whose office plants have died.",
        "I told the doctor I broke my leg in two places. He told me to quit going to those places.",
        "Why do Americans choose from just two people to run for president and 50 for Miss America?",
        "Knowledge is knowing a tomato is a fruit; Wisdom is not putting it in a fruit salad.",
        "Better to remain silent and be thought a fool, than to speak and remove all doubt."]
running =True
while running:
    click = False
    for e in event.get():
        if e.type == QUIT:
            running = False
        if e.type == MOUSEBUTTONDOWN:
            click = True
            
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()

    if click:
        txtPic = comicFont.render(choice(quotes), True, (255,0,0))
        screen.blit(txtPic,(mx-txtPic.get_width()/2, my-txtPic.get_height()/2))
    if mb[2]==1:
        screen.fill((0,0,0))
    display.flip()

font.quit()
del comicFont
quit()
