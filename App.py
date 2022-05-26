import pygame
from pygame import mixer

pygame.init()

width = 1200
height = 700

black = (0,0,0)
white = (255,255,255)
grey = (128,128,128)

#set the screen/window
screen = pygame.display.set_mode([width,height])
pygame.display.set_caption("SICKO MODE")

label_font = pygame.font.Font('WigendaTypewrite.ttf',32)
fps = 60
timer = pygame.time.Clock()


start = True

while start :
    timer.tick(fps)
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start  = False
    

    pygame.display.flip()


pygame.quit()
