import pygame
from pygame import MOUSEBUTTONDOWN, mixer

pygame.init()

width = 1400
height = 800

black = (0,0,0)
white = (255,255,255)
grey = (128,128,128)
green = (0,255,0)
gold = (212,175,55)

#set the screen/window
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("SICKO MODE")

label_font = pygame.font.Font('WigendaTypewrite.ttf',30)
fps = 60
beats = 8
sounds = 6
boxes=[]
clicked = [[-1 for i in range(beats)]  for i in range(sounds)] 
timer = pygame.time.Clock()


def drawGrid() :
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
            if clicked[j][i] == -1 :
                color = grey
            else :
                color = green

            rect = pygame.draw.rect(screen,color,[i*(width-200)//beats+205,(j*100)+5,(width-200)//beats-10,((height-200)//sounds)],0,3)

            pygame.draw.rect(screen,black,[i*(width-200)//beats+200,(j*100),(width-200)//beats,((height-200)//sounds)],3,3)
            pygame.draw.rect(screen,gold,[i*(width-200)//beats+200,(j*100),(width-200)//beats,((height-200)//sounds)],3,3)
            
            boxes.append((rect,(i,j)))

    return boxes



start = True

while start :
    timer.tick(fps)
    screen.fill(black)

    boxes = drawGrid()  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start  = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].colliderect(event.pos) :
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1


    pygame.display.flip()


pygame.quit()
