import pygame
import time
from pygame import MOUSEBUTTONDOWN, MOUSEBUTTONUP, mixer


pygame.init()

width = 1400
height = 800

black = (0, 0, 0)
darkGrey = (50, 50, 50)
white = (255, 255, 255)
grey = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

# set the screen/window
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("DR. BEATZ")

label_font = pygame.font.Font('WigendaTypewrite.ttf', 30)
mediumFont = pygame.font.Font('WigendaTypewrite.ttf', 24)
fps = 60
beats = 8
sounds = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(sounds)]
activeList = [1 for _ in range(sounds) ]
activeLength = 0
activeBeat = 0
bpm = 240
beatChanged = True
Playing = True
start = True
timer = pygame.time.Clock()

# loading sounds
hi_hat = mixer.Sound('sounds\hi hat.WAV')
crash = mixer.Sound('sounds\crash.WAV')
clap = mixer.Sound('sounds\clap.WAV')
kick = mixer.Sound('sounds\kick.WAV')
snare = mixer.Sound('sounds\snare.WAV')
tom = mixer.Sound('sounds\\tom.WAV')
pygame.mixer.set_num_channels(sounds*3)


def play_note():
    for i in range(len(clicked)):
        if clicked[i][activeBeat] == 1:
            if i == 0 and activeList[i] == 1:
                hi_hat.play()
            if i == 1 and activeList[i] == 1:
                snare.play()
            if i == 2 and activeList[i] == 1:
                kick.play()
            if i == 3 and activeList[i] == 1:
                crash.play()
            if i == 4 and activeList[i] == 1:
                clap.play()
            if i == 5 and activeList[i] == 1:
                tom.play()


def drawGrid(clicked, activeBeat, actives):
    global label_font, fps, beats, sounds, boxes, timer
    left_box = pygame.draw.rect(screen, grey, [0, 0, 200, height-200], 5)
    bottom_box = pygame.draw.rect(screen, grey, [0, height-200, width, 200], 5)
    boxes = []
    colours = [grey, white, grey]
    hi_hatText = label_font.render('Hi Hat', True, colours[actives[0]])
    screen.blit(hi_hatText, (30, 30))
    snareText = label_font.render('Snare', True, colours[actives[1]])
    screen.blit(snareText, (30, 130))
    KickText = label_font.render('Bass Drum', True, colours[actives[2]])
    screen.blit(KickText, (30, 230))
    CrachText = label_font.render('Crash', True, colours[actives[3]])
    screen.blit(CrachText, (30, 330))
    ClapText = label_font.render('Clap', True, colours[actives[4]])
    screen.blit(ClapText, (30, 430))
    FloorText = label_font.render('Floor Tom', True, colours[actives[5]])
    screen.blit(FloorText, (30, 530))

    for i in range(6):
        pygame.draw.line(screen, grey, (0, ((i*100)+100)),
                         (200, ((i*100)+100)), 5)

    for i in range(beats):
        for j in range(sounds):
            if clicked[j][i] == -1:
                color = grey
            else:
                if actives[j] == 1:
                    color = green
                else:
                    color = darkGrey
                # color = green

            rect = pygame.draw.rect(screen, color, [
                                    i*(width-200)//beats+205, (j*100)+5, (width-200)//beats-10, ((height-200)//sounds)], 0, 3)

            pygame.draw.rect(screen, gold, [
                             i*(width-200)//beats+200, (j*100), (width-200)//beats, ((height-200)//sounds)], 3, 3)
            pygame.draw.rect(screen, black, [
                             i*(width-200)//beats+200, (j*100), (width-200)//beats, ((height-200)//sounds)], 1, 1)

            boxes.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [
                                  activeBeat * ((width - 200) // beats) + 200, 0, ((width - 200) // beats), sounds * 100], 3, 3)

    return boxes


while start:
    timer.tick(fps)
    screen.fill(black)

    boxes = drawGrid(clicked, activeBeat, activeList)
    # lower menu
    playPause = pygame.draw.rect(
        screen, grey, [50, height-150, 200, 100], 0, 5)
    playText = label_font.render('Play/Pause', True, white)
    screen.blit(playText, (70, height-130))
    if Playing:
        playText2 = mediumFont.render('Playing', True, darkGrey)
    else:
        playText2 = mediumFont.render('Paused', True, darkGrey)
    screen.blit(playText2, (70, height-100))

    # BPM alterations
    bpmRect = pygame.draw.rect(screen, grey, [300, height-150, 200, 100], 5, 5)
    bpmText = mediumFont.render('Beats per min', True, white)
    screen.blit(bpmText, (310, height-130))
    bpmText2 = label_font.render(f'{bpm}', True, white)
    screen.blit(bpmText2, (370, height-100))

    bpmUp = pygame.draw.rect(screen, grey, [510, height-150, 48, 48], 0, 5)
    bpmDown = pygame.draw.rect(screen, grey, [510, height-100, 48, 48], 0, 5)
    Uptext = mediumFont.render('+5', True, white)
    DownText = mediumFont.render('-5', True, white)
    screen.blit(Uptext, (520, height-140))
    screen.blit(DownText, (520, height-90))

    #Beats adding 
    beatsRect = pygame.draw.rect(screen, grey, [600, height-150, 200, 100], 5, 5)
    beatsText = mediumFont.render('Beats in loop', True, white)
    screen.blit(bpmText, (610, height-130))
    bpmText2 = label_font.render(f'{beats}', True, white)
    screen.blit(bpmText2, (670, height-100))

    beatsUp = pygame.draw.rect(screen, grey, [810, height-150, 48, 48], 0, 5)
    beatsDown = pygame.draw.rect(screen, grey, [810, height-100, 48, 48], 0, 5)
    UptextBeats = mediumFont.render('+1', True, white)
    DownTextBeats = mediumFont.render('-1', True, white)
    screen.blit(UptextBeats, (820, height-140))
    screen.blit(DownTextBeats, (820, height-90))

    #instrument rects
    sound_rect = []
    for i in range(sounds):
        rect = pygame.rect.Rect((0, 100*i), (200,100))
        sound_rect.append(rect)

    if beatChanged:
        play_note()
        beatChanged = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

        if event.type == pygame.MOUSEBUTTONUP:
            if playPause.collidepoint(event.pos):
                if Playing:
                    Playing = False
                elif not Playing:
                    Playing = True
            elif bpmUp.collidepoint(event.pos):
                bpm = bpm + 5
            elif bpmDown.collidepoint(event.pos):
                bpm = bpm - 5 
            elif beatsDown.collidepoint(event.pos):
                beats = beats - 1 
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            elif beatsUp.collidepoint(event.pos):
                beats = beats + 1  
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            for i in range(len(sound_rect)):
                if sound_rect[i].collidepoint(event.pos):
                    activeList[i] *= -1 ; 



    beatLength = 3600//bpm

    if Playing:
        if activeLength < beatLength:
            activeLength += 1
        else:
            activeLength = 0
            if activeBeat < beats-1:
                activeBeat += 1
                beatChanged = True
            else:
                activeBeat = 0
                beatChanged = True

    pygame.display.flip()


pygame.quit()
