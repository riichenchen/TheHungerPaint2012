#The Hunger Paint
#Chen~
'''This program allows a user to draw on a canvas. There are a variety of tools
available for use. The user can load or save images to file. The tools included
are: Pencil, Eraser, Paintbrush, Fill Bucket, Airbrush, Stamps, Clone Stamp,
Rectangular Marquee, and Polygons.'''

from random import *
from pygame import *
from glob import *

#====================================Setup=====================================#
"Screen,Intro,Background,Font,Canvas,Color Spectrum,Functional Images, etc."
screen=display.set_mode((1024,768))

init()
for i in range (2):
    mixer.music.load("songs/song%d.mp3"%i)
mixer.music.play(-1)
player=[image.load("images/play.png"),image.load("images/pause.png")]
button=1

screen.blit(image.load("images/intro.png"),(0,0))
display.flip()                                      
time.wait(2500)                                    
running=True

screen.blit(image.load("images/the hunger paint2.png"),(0,0))
grill=image.load("images/grill.png")
loading=image.load("images/save.png")
loadgood=image.load("images/load success.png")
loadbad=image.load("images/load failed.png")
saving=image.load("images/load.png")
saved=image.load("images/save success.png")

font.init()
comicFont = font.SysFont("Comic Sans MS", 20)
colorspectrum=Rect(655,578,983-655,667-578)
canvasRect=Rect(276,106,709,446)
draw.rect(screen,(255,255,255),canvasRect,0)
mouse.set_visible(False)

#================================Loading Images================================#
stamps,thumbnails,thumbnailRects=[],[],[]
tools,toolRects,tooltexts,polygonsRects,polygons,cursors=[],[],[],[],[],[]
#Stamps & Thumbnails
for i in range (4):
    stamps+=[image.load("images/stamps/stamp%d.png"%(i))]
    thumbnails+=[image.load("images/thumbnails/thumbnail%d.png"%(i))]
    thumbnailRects+=[Rect(289+60*i,574,50,50)]
for i in range (4,8):           #Two loops since the y value changes
    stamps+=[image.load("images/stamps/stamp%d.png"%i)]
    thumbnails+=[image.load("images/thumbnails/thumbnail%d.png"%i)]
    thumbnailRects+=[Rect(289+60*(i-4),634,50,50)]
    
#Cursors
for i in range (12):
    cursors+=[image.load("images/cursors/cursor%d.png"%i)]
##cursors+=cursors[2]             #For the color spectrum

#Tool Icons & Text
"Tools - Drawing tools. Fixed Tools - Undo, Load, Save, etc."
for i in range (0,10,2):        #Jumping to accomodate for change in x
    tools+=[image.load("images/tools/tool%d.png"%i)]
    tools+=[image.load("images/tools/tool%d.png"%(i+1))]
    toolRects+=[Rect(91,424+30*i,49,49)]
    toolRects+=[Rect(157,424+30*i,49,49)]
    tooltexts+=[image.load("images/tooltext/text%d.png"%i)]
    tooltexts+=[image.load("images/tooltext/text%d.png"%(i+1))]
for i in range (5):             #The fixedtools have different Rects.
    tools+=[image.load("images/fixedtools/fixedtool%d.png"%i)]
    tooltexts+=[image.load("images/tooltext/ftext%d.png"%i)]
    toolRects+=[Rect(651+62*i,693,53,25)]

#Polygon Icons
for i in range (6):
    polygons+=[image.load("images/polygons/polygon%d.png"%i)]
    polygonsRects+=[Rect(287+57*i,574,50,50)]

#Initial/Default Values
color=(0,0,0)
tool=stampno=polygonno=0            #Using indices & related lists
chen=bfound=False
size=3
sizes=["XS","S","M","L","XL"]
canvasb=screen.subsurface(canvasRect).copy()
fpolygon=[]
clone=""
movex,movey=0,0
found=False
shiftx,shifty=0,0
moving=False
moved=False
copy=""
undos=[canvasb]
redos=[]
painted=False

#==================================Functions==================================#
'''These functions do the "housework" -- resetting values, getting positions &
    states, adjusting sizes/color, running things, etc.'''

def reset():                #Reset values that must be updated each iteration
    global mx,my,mb,click,rclick, release,rrelease,cursorb,shift,alt,painted
    screen.set_clip(None)
    shift=alt=rrelease=release=click=rclick=False
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
        
    
def getEvent():             #Get Events and any markers related to the events
    global running,click,release,size,clickx,clicky,rrelease,rclick,shift,alt
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==MOUSEBUTTONUP:
            if evt.button==1:
                release=True
            if evt.button==3:
                rrelease==True
        if evt.type==MOUSEBUTTONDOWN:
            if evt.button==1:
                click=True
                clickx,clicky=evt.pos
            if evt.button==3:
                rclick=True
            if evt.button==4 and size<5:
                size+=1
            if evt.button == 5 and size>1:
                size-=1
    keys=key.get_pressed()
    if keys[K_RSHIFT] or keys[K_LSHIFT]:
        shift=True
    if keys[K_RALT] or keys[K_LALT]:
        alt=True
                
def drawStuff():                #Draw the buttons, color indicator, text
    screen.blit(grill,(275,562))
    for i in range (len(toolRects)):            #Tools
        screen.blit(tools[i],toolRects[i])
    screen.blit(player[button],(962,693))       #Music
    draw.circle(screen,color,(988,47),30)       #Color indicator
    draw.circle(screen,(255,255,255),(988,47),30,2)
    
    txtPic = comicFont.render("(%d,%d) Size %s"%(mx,my,sizes[size-1]),True,\
                              (255,255,255))
    draw.rect(screen, (0,0,0),(792,732,250,30))
    screen.blit(txtPic,(792,732))           #Position & Size indicators

def getTool(x,y):               #Tool selection
    global tool,area,shiftx,shifty
    draw.rect(screen,(0,255,255),toolRects[tool],2)
    draw.rect(screen,(247,249,248),(66,288,177,87))     #Clear the text area
    screen.blit(tooltexts[tool],(66,288))
    for i in range (len(toolRects)):
        if toolRects[i].collidepoint(x,y):
            draw.rect(screen,(255,0,0),toolRects[i],2)
            draw.rect(screen,(247,249,248),(66,288,177,87))
            screen.blit(tooltexts[i],(66,288))
            if click and i<10:          #We don't consider the fixed tools
                tool=i
                    
def getName(image,textArea):
    ans = ""
    back = screen.copy()        
    typing = True
    while typing:
        for e in event.get():
            if e.type == QUIT:
                event.post(e)   # puts QUIT back in event list so main quits
                return ""
            if e.type == KEYDOWN:           
                if e.key == K_BACKSPACE:
                    if len(ans)>0:
                        ans = ans[:-1]
                elif e.key == K_KP_ENTER or e.key == K_RETURN : 
                    typing = False
                elif e.key<256:
                    ans += e.unicode
        txtPic = comicFont.render(ans, True, (0,0,0))
        screen.blit(image,(400,300))
        draw.rect(screen,(220,255,220),textArea)
        draw.rect(screen,(0,0,0),textArea,2)            
        screen.blit(txtPic,(textArea.x+3,textArea.y+2))        
        display.flip()
    screen.blit(back,(0,0))
    return ans

def paint():                    #Runs all the Painting Functions & Load/Save
    global mx,my,color,size,undos,redos,click,release,rrelease,canvasb,copy
    global painted,allb,back,found,area
    
    if click and found and area.collidepoint(mx,my)==False:
        resetMarquee()
    if colorspectrum.collidepoint(mx,my) and click:
        color=screen.get_at((mx,my))[:3]
    if click and toolRects[13].collidepoint(mx,my) and len(undos)>1:
        undo()
    if click and toolRects[14].collidepoint(mx,my) and len(redos)>0:
        redo()
    if click and toolRects[10].collidepoint(mx,my):
        clear()
    if click and toolRects[11].collidepoint(mx,my):
        load()
        fire()
        canvasb=screen.subsurface(canvasRect).copy()
    if click and toolRects[12].collidepoint(mx,my):
        save()
    if mb[0]==1 and tool==2:
        color=screen.get_at((mx,my))[:3]
    if tool==7:
        stamp(mx,my)
    if tool==5:
        polygon(mx,my,color,size)
    if canvasRect.collidepoint(mx,my):
        screen.set_clip(canvasRect)
        if mb[0]==1 and tool!=8 and not alt:        #If there's been a change
            painted=True
        if mb[0]==1 and tool==0:
            pencil(mx,my,size,color)
        if mb[0]==1 and tool==1:
            eraser(mx,my,size*5)
        if mb[0]==1 and tool==4:
            airbrush (size*20,color,mx,my)
        if tool==6 and release:
            ffill(mx,my,screen.get_at((mx,my))[:3],color)
        if tool==3 and mb[0]==1:
            brush(mx,my,size*5,color)
        if tool==8:
            rectselect(mx,my)
        if tool==9:
            clonestamp(mx,my,size*5)
        if release and tool!=2 and tool!=8:         #8 does not work with undo
            fire()
    cond=canvasRect.collidepoint(mx,my)==alt==False
    if cond and release and painted and tool!=2 and tool!=8:
        fire()                  #In case they release outside the canvas
    if release or rclick:
        canvasb=screen.subsurface(canvasRect).copy()    #Back of canvas
        allb=screen.copy()                              #Back of whole screeen
        
def blitcursor():               #Blits the cursor
    cursorb=screen.copy()           #Copy the screen BEFORE blitting cursor
    if tool==5 or tool==7 or tool==8:
        screen.blit(cursors[tool],(mx-10,my-10))
    elif tool==9:               #Clone stamp cursors
        if alt:
            screen.blit(cursors[10],(mx-10,my-10))
        else:
            screen.blit(cursors[9],(mx-20,my-20))
        if bfound and mb[0]==1 and not alt:
            screen.blit(cursors[11],(bx-10,by-10))
    else:
        screen.blit(cursors[tool],(mx,my-20))
    display.flip()                  #Flip the screen with cursor, THEN
    screen.blit(cursorb,(0,0))      #restore the screen to previous state

def manageMusic(x,y):
    global button
    if Rect(962,693,25,25).collidepoint(x,y):
        draw.rect(screen,(255,0,0),Rect(962,693,25,25),2)
        if click and button==1:
            mixer.music.pause()
            button=0
        elif click and button==0:
            mixer.music.unpause()
            button=1

#==============================Painting Functions==============================#
'''These functions are the actual paint tools'''
def resetMarquee():
    global moving,found,back,select,area,shiftx,shifty,copy,moved
    moving=found=False
    screen.blit(back,(0,0))
    screen.blit(select,area)
    shiftx,shifty=0,0
    copy=""
def getArea(nmx,nmy):
    global area,select,back,moving,shiftx,shifty,copy,found
    found=True
    area=Rect(clickx,clicky,nmx-clickx,nmy-clicky-1)
    area.normalize()
    select=copy.subsurface(area).copy()
    screen.blit(copy,(0,0))
    draw.rect(screen,(255,255,255),area,0)
    back=screen.copy()              #New screen without the selection
    screen.blit(select,area)
    draw.rect(screen,(111,111,111),area,1)
def rectselect(mx,my):
    global area,select,back,moving,shiftx,shifty,copy,found,moved
    nmx,nmy=mouse.get_pos()
    if found==False and mb[0]==1:
        if copy=="":                #A deep copy to avoid selecting the box
            copy=screen.copy()
        screen.blit(canvasb,canvasRect)
        draw.rect(screen,(111,111,111),(clickx,clicky,nmx-clickx,nmy-clicky),1)
        if release:
            getArea(nmx,nmy)
    elif found:
        if area.collidepoint(mx,my) and mb[0]==1:
            moving=True
            if (shiftx,shifty)==(0,0):      #The offset
                shiftx,shifty=clickx-area[0],clicky-area[1]
        if moving and mb[0]==1:
            screen.blit(back,(0,0))
            screen.blit(select,area)
            draw.rect(screen,(111,111,111),area,1)
            area=Rect(mx-shiftx,my-shifty,area[2],area[3])
        
def pencil(x,y,thickness, color):
    mxn,myn=mouse.get_pos()
    draw.line(screen,color,(x,y),(mxn,myn),thickness)

def eraser (x,y,thickness):
    nmx,nmy=mouse.get_pos()
    dist=((nmx-x)**2+(nmy-y)**2)**0.5
    if dist==0:dist=1
    sx,sy=(nmx-x)/dist,(nmy-y)/dist
    for i in range (int(dist)+1):
        draw.circle(screen,(255,255,255),(int(x+i*sx),int(y+i*sy)),thickness)

def airbrush(radius, color,mx,my):
    for i in range (radius/2):          #To speed up the airbrush
        size=randint (0,radius/10)
        x,y=randint(-1*radius,radius),randint(-1*radius,radius)
        if x**2+y**2<radius**2:
            draw.circle(screen, color, (mx+x, my+y), size)

def ffill (x,y,old, new):
    pts=[(x,y)]
    while len(pts)>0:
        pt=pts.pop()
        nx,ny=pt[0],pt[1]
        if -1<nx<1024 and -1<ny<768 and screen.get_at((nx,ny))[:3]==old:
            screen.set_at((nx,ny),new)
            pts+=[(nx-1,ny),(nx+1,ny),(nx,ny-1),(nx,ny+1)]

def fire():                     #Takes a snapshot for undo/redo. Yes, fire.
    global undos, redos, painted
    undos+=[screen.subsurface(canvasRect).copy()]
    if len(undos)>20:           #Control the depth of the undo.
        del undos[0]
    redos=[]
    painted=False

def undo():
    global redos, undos
    redos+=[undos.pop()]
    screen.blit(undos[-1],canvasRect)       #Blit the previous snapshot

def redo():
    global undos, redos
    undos+=[redos.pop()]
    screen.blit(undos[-1],canvasRect)       #Blit the snapshot we just redid.

def stamp(x,y):
    global stampno
    for i in range(8):                      #Getting the right stamp
        screen.blit(thumbnails[i],thumbnailRects[i])
    draw.rect(screen,(0,255,255),thumbnailRects[stampno],2)
    for i in range (8):
        if thumbnailRects[i].collidepoint(x,y):
            draw.rect(screen,(255,0,0),thumbnailRects[i],2)
            if click:
                stampno=i
    if canvasRect.collidepoint(x,y) and mb[0]==1:   #Using the stamp
        screen.blit(canvasb,canvasRect)
        screen.set_clip(canvasRect)
        screen.blit(stamps[stampno],(x-(stamps[stampno].get_width())/2,\
                                     y-(stamps[stampno].get_height())/2))
    
def clonestamp(x,y,size):
    global movex,movey,clone,bfound,bx,by
    nmx,nmy=mouse.get_pos()
    if alt and click:                   #Initial buffer point
        clone=(clickx,clicky)
        movex,movey=0,0
    if clone!="" and (movex,movey)==(0,0) and click:    #Initial shift
        movex,movey=clickx-clone[0],clicky-clone[1]
    if mb[0]==1 and clone!="" and (movex,movey)!=(0,0):
        bfound=True                     #If buffer's found; for cursor
        bx,by=x-movex,y-movey
        nbx,nby=nmx-movex,nmy-movey
        bounded=Rect(canvasRect[0]+size/2,canvasRect[1]+size/2,     #To stay
                     canvasRect[2]-size,canvasRect[3]-size)         #on screen
        if bounded.collidepoint(bx,by) and bounded.collidepoint(nbx,nby):
            dist=((nmx-x)**2+(nmy-y)**2)**0.5
            if dist==0:
                buffRect=Rect(bx-size/2,by-size/2,size,size)   
                buff=screen.subsurface(buffRect).copy()        #Copy at buffer  
                screen.blit(buff,(x-size/2,y-size/2))
            else:
                sx,sy=(nmx-x)/dist,(nmy-y)/dist
                for i in range (int(dist)+1):
                    buffRect=Rect(bx-size/2+i*sx,by-size/2+i*sy,size,size)
                    buff=screen.subsurface(buffRect).copy()
                    screen.blit(buff,(x-size/2+i*sx,y-size/2+i*sy))

def brush(x,y,thickness, color):
    nmx,nmy=mouse.get_pos()
    dist=((nmx-x)**2+(nmy-y)**2)**0.5
    if dist==0:
        dist=1
    sx,sy=(nmx-x)/dist,(nmy-y)/dist
    for i in range (int(dist)+1):
        draw.circle(screen,color,(int(x+i*sx),int(y+i*sy)),thickness)
        
def polygon(x,y, color, thickness):
    global polygonno,fpolygon
    for i in range(6):                  #Getting the right shape
        screen.blit(polygons[i],polygonsRects[i])
        if polygonsRects[i].collidepoint(x,y):
            draw.rect(screen,(255,0,0),polygonsRects[i],2)
            if click:
                polygonno=i
    draw.rect(screen,(0,255,255),polygonsRects[polygonno],2)

    if canvasRect.collidepoint(x,y) and mb[0]==1:   #Drawing the shape
        nmx,nmy=mouse.get_pos()
        screen.blit(canvasb,canvasRect)
        screen.set_clip(canvasRect)
        if polygonno==0:        #Line
            draw.line(screen,color,(clickx,clicky),(nmx,nmy),thickness)
        elif polygonno==1:      #Unfilled Ellipse
            cornerx,cornery=min(clickx, nmx),min(clicky,nmy)
            if shift:               #Circle
                r=min(abs(clickx-nmx),abs(clicky-nmy))
                cornerx,cornery=max(clickx-r,cornerx),max(clicky-r,cornery)
                    #To keep the corner from moving to the right
                draw.ellipse(screen,color,(cornerx,cornery,r+thickness*2,\
                                           r+thickness*2),thickness)
            else:
                w,h=abs(clickx-nmx)+thickness*2,abs(clicky-nmy)+thickness*2
                draw.ellipse(screen,color,(cornerx,cornery,w,h),thickness)
        elif polygonno==2:      #Filled Ellipse
            cornerx,cornery=min(clickx, nmx),min(clicky,nmy)
            if shift:               #Circle
                r=min(abs(clickx-nmx),abs(clicky-nmy))
                cornerx,cornery=max(clickx-r,cornerx),max(clicky-r,cornery)
                draw.ellipse(screen,color,(cornerx,cornery,r,r),0)
            else:
                w,h=abs(clickx-nmx),abs(clicky-nmy)
                draw.ellipse(screen,color,(cornerx,cornery,w,h),0)
        elif polygonno==3:      #Unfilled Rect
            if shift and nmx-clickx!=0 and nmy-clicky!=0:     #Square
                lx,ly=nmx-clickx,nmy-clicky
                px,py=lx/abs(lx),ly/abs(ly)                 #Find direction
                s=min(abs(nmx-clickx),abs(nmy-clicky))  #Side length
                draw.rect(screen,color,(clickx,clicky,s*px,s*py),thickness)
            else:
                draw.rect(screen,color,(clickx,clicky,nmx-clickx,nmy-clicky),\
                          thickness)
        elif polygonno==4:      #Filled Rect
            if shift and nmx-clickx!=0 and nmy-clicky!=0:     #Square
                lx,ly=nmx-clickx,nmy-clicky
                px,py=lx/abs(lx),ly/abs(ly)
                s=min(abs(nmx-clickx),abs(nmy-clicky))
                draw.rect(screen,color,(clickx,clicky,s*px,s*py),0)
            else:
                draw.rect(screen,color,(clickx,clicky,nmx-clickx,nmy-clicky),0)
        elif polygonno==5:      #Freeform Polygon
            if fpolygon==[]:    #To make sure the list is never blank
                fpolygon+=[(clickx,clicky)]
            draw.lines(screen, color, False, fpolygon+[(nmx,nmy)],thickness)
            if release:
                fpolygon+=[(nmx,nmy)]
    if rclick and len(fpolygon)>1:      #Outside if to satisfy "mb[0]==1"
        draw.lines(screen,color,True,fpolygon,thickness)
        fpolygon=[]                     #Close polygon and reset list

def clear():
    global running, chen            #'Cause I'm just that awesome :P
    if randint(0,9)==0:
        chen=True
        running=False
    draw.rect(screen, (255,255,255),canvasRect)

#==================================LOAD/SAVE===================================#
def load():
    back=screen.copy()
    pics = glob("*.bmp")+glob("*.jpg")+glob("*.png")
    n = len(pics)
    if n>14:                        #Keep list of images onscreen
        pics=pics[:14]
        n=14
    choiceArea = Rect(725,100,270,len(pics)*40)
    draw.rect(screen,(220,220,220),choiceArea)       
    draw.rect(screen,(0,0,0),choiceArea,1)  
    for i in range(n):
        txtPic = comicFont.render(pics[i], True, (0,111,0)) 
        screen.blit(txtPic,(725+3,40*i+100))
    name=getName(loading,Rect(413,463,270,40))
    notgiveup=waiting=True
    while notgiveup:                #In case people can't type...
        try:
            bg=image.load(name)
            break                   #Break the loop w/o changing flag
        except:
            name=getName(loadbad,Rect(413,463,270,40))
            if name=="quit":
                bg=back.subsurface(canvasRect).copy()
                notgiveup=False
    while waiting and notgiveup:    #A waiting "success" dialogue box
        for e in event.get():
            if e.type == QUIT:
                event.post(e)
                waiting=False
            if e.type == KEYDOWN:           
                if e.key == K_KP_ENTER or e.key == K_RETURN:
                    waiting = False
        screen.blit(loadgood,(400,300))
        display.flip()
    screen.blit(back,(0,0))
    screen.blit(bg,canvasRect)

def save():
    back=screen.copy()
    name=getName(saving,Rect(413,463,270,40)).lower()
    if name.find(".bmp")+name.find(".png")+name.find(".jpg")==-3:
        name+=".jpg"
    image.save(screen.subsurface(canvasRect),name)
    waiting=True
    while waiting:
        for e in event.get():
            if e.type == QUIT:
                event.post(e)
                waiting=False
            if e.type == KEYDOWN:           
                if e.key == K_KP_ENTER or e.key == K_RETURN:
                    waiting = False
        screen.blit(saved,(400,300))
        display.flip()
    screen.blit(back,(0,0))
#=====================================Main=====================================#
while running:
    reset()
    getEvent()
    drawStuff()
    getTool(mx,my)
    manageMusic(mx,my)
    paint()
    blitcursor()
#=====================================Chen=====================================#
"I just had to. I really did."

while chen:
    for evt in event.get():
        if evt.type==QUIT:
            chen=False
    screen.fill((255,255,255))
    text="Ugh. We ran out of decoy dinners.Sorry about that. We'll fix this ASAP."
    text2="Please just quit the program for now and come back in a bit =]"
    text3="Also, any food donations will be much appreciated for future uses."
    txtPic = comicFont.render(text, True, (0,0,0))
    screen.blit(txtPic,(200,350))
    txtPic = comicFont.render(text2, True, (0,0,0))
    screen.blit(txtPic,(200,370))
    txtPic = comicFont.render(text3, True, (0,0,0))
    screen.blit(txtPic,(200,390))
    display.flip()

quit()
