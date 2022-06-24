import pygame, time
from pygame import MOUSEBUTTONDOWN, mixer


pygame.init()

width = 1400
height = 800

black = (0,0,0)
white = (255,255,255)
grey = (128,128,128)
green = (0,255,0)
gold = (212,175,55)
blue = (0,255,255)

#set the screen/window
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("SICKO MODE")

label_font = pygame.font.Font('WigendaTypewrite.ttf', 30)
fps = 60
beats = 8
sounds = 6
boxes=[]
clicked = [[-1 for _ in range(beats)] for _ in range(sounds)]
activeLength = 0
activeBeat = 0
bpm = 240 
beatChanged = True
Playing = True
start = True
timer = pygame.time.Clock()


def drawGrid(clicked,activeBeat) :
    global label_font, fps, beats, sounds, boxes, timer
    left_box = pygame.draw.rect(screen,grey,[0,0,200,height-200],5)
    bottom_box = pygame.draw.rect(screen,grey,[0,height-200,width,200],5)
    boxes = []
    colours = [grey,white,grey]
    hi_hatText = label_font.render('HI HAT',True,white)
    screen.blit(hi_hatText,(30,30))
    snareText = label_font.render('Snare',True,white)
    screen.blit(snareText,(30,130))
    KickText = label_font.render('Bass Drum',True,white)
    screen.blit(KickText,(30,230))
    CrachText = label_font.render('Crash',True,white)
    screen.blit(CrachText,(30,330))
    ClapText = label_font.render('Clap',True,white)
    screen.blit(ClapText,(30,430))
    FloorText = label_font.render('Floor Tom',True,white)
    screen.blit(FloorText,(30,530))

    for i in range(6):
        pygame.draw.line(screen,grey,(0,((i*100)+100)),(200,((i*100)+100)),5)

    for i in range(beats):
        for j in range(sounds):
            if clicked[j][i] == -1:
                color = grey
            else  :
                color = green

            rect = pygame.draw.rect(screen,color,[i*(width-200)//beats+205,(j*100)+5,(width-200)//beats-10,((height-200)//sounds)],0,3)

            pygame.draw.rect(screen,gold,[i*(width-200)//beats+200,(j*100),(width-200)//beats,((height-200)//sounds)],3,3)
            pygame.draw.rect(screen,black,[i*(width-200)//beats+200,(j*100),(width-200)//beats,((height-200)//sounds)],1,1)
            
            boxes.append((rect,(i,j)))
        
        
        active = pygame.draw.rect(screen, blue,[activeBeat * ((width - 200) // beats) + 200, 0, ((width - 200) // beats), sounds * 100],3,3)

    return boxes


while start :
    timer.tick(fps)
    screen.fill(black)

    boxes = drawGrid(clicked,activeBeat)  

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            start  = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos) :
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

    beatLength = 3600//bpm

    if Playing :
        if activeLength < beatLength:
            activeLength += 1
        else :
            activeLength = 0
            if activeBeat < beats-1 :
                activeBeat += 1 
                beatChanged = True
            else:
                activeBeat = 0
                beatChanged = True

    pygame.display.flip()


pygame.quit()
