# from json import load
import pygame
import time
from pygame import K_BACKSPACE, MOUSEBUTTONDOWN, MOUSEBUTTONUP, mixer
from pyparsing import White


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
lightGrey = (170, 170, 170)

# set the screen/window
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("DR. BEATZ")

label_font = pygame.font.Font('WigendaTypewrite.ttf', 30)
mediumFont = pygame.font.Font('WigendaTypewrite.ttf', 24)
index = 100
fps = 60
beats = 8
sounds = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(sounds)]
activeList = [1 for _ in range(sounds)]
activeLength = 0
activeBeat = 0
bpm = 240
beatChanged = True
Playing = True
start = True
beat_name = ''
typing = False

SaveMenu = False
LoadMenu = False
savedBeats = []
file = open('SavedBeats.txt', 'r')
for line in file:
    savedBeats.append(line)

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


def draw_LoadMenu(index):
    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pygame.draw.rect(screen, black, [0, 0, width, height])
    menu_text = label_font.render(
        'LOAD MENU: Select a beat to load in', True, white)
    screen.blit(menu_text, (400, 40))
    exit_btn = pygame.draw.rect(
        screen, grey, [width - 200, height - 100, 180, 90], 0, 5)
    exit_text = label_font.render('Close', True, white)
    screen.blit(exit_text, (width - 160, height - 70))
    loading_btn = pygame.draw.rect(
        screen, grey, [width // 2 - 100, height * 0.87, 200, 100], 0, 5)
    loading_text = label_font.render('Load Beat', True, white)
    screen.blit(loading_text, (width // 2 - 70, height * 0.87 + 30))
    delete_btn = pygame.draw.rect(
        screen, grey, [width // 2 - 400, height * 0.87, 200, 100], 0, 5)
    delete_text = label_font.render('Delete Beat', True, white)
    screen.blit(delete_text, (width // 2 - 385, height * 0.87 + 30))
    if 0 <= index < len(savedBeats):
        pygame.draw.rect(screen, lightGrey, [190, 100 + index*50, 1000, 50])
    for beat in range(len(savedBeats)):
        if beat < 10:
            beat_clicked = []
            row_text = mediumFont.render(f'{beat + 1}', True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = savedBeats[beat].index('name: ') + 6
            name_index_end = savedBeats[beat].index(', beats:')
            name_text = mediumFont.render(
                savedBeats[beat][name_index_start:name_index_end], True, white)
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(savedBeats) and beat == index:
            beats_index_end = savedBeats[beat].index(', bpm:')
            loaded_beats = int(
                savedBeats[beat][name_index_end + 8:beats_index_end])
            bpm_index_end = savedBeats[beat].index(', selected:')
            loaded_bpm = int(
                savedBeats[beat][beats_index_end + 6:bpm_index_end])
            loaded_clicks_string = savedBeats[beat][bpm_index_end + 14: -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = (loaded_clicks_rows[row].split(', '))
                for item in range(len(loaded_clicks_row)):
                    if loaded_clicks_row[item] == '1' or loaded_clicks_row[item] == '-1':
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rect = pygame.draw.rect(screen, grey, [190, 90, 1000, 600], 5, 5)
    return exit_btn, loading_btn, entry_rect, delete_btn, loaded_info


def draw_SaveMenu(beat_name, typing):
    pygame.draw.rect(screen, black, [0, 0, width, height])
    menuText = label_font.render(
        'SAVE MENU: Enter name of the beat.', True, white)
    screen.blit(menuText, (400, 40))

    SavingButton = pygame.draw.rect(
        screen, grey, [width//2 - 165, height*0.75 + 18, 400, 100], 0, 5)
    SavingButtonText = label_font.render('Save Beat', True, white)
    screen.blit(SavingButtonText, (width//2 - 35, height * 0.75 + 50))
    exitBtn = pygame.draw.rect(
        screen, grey, [width-200, height-100, 180, 90], 0, 5)
    exitText = label_font.render('Close', True, white)
    screen.blit(exitText, (width-150, height-70))

    if typing:
        pygame.draw.rect(screen, darkGrey, [400, 200, 600, 200], 0, 5)

    entry_rect = pygame.draw.rect(screen, grey, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text, (430, 250))
    return exitBtn, SavingButton, entry_rect


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

    # Beats adding
    beatsRect = pygame.draw.rect(
        screen, grey, [600, height-150, 200, 100], 5, 5)
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

    # instrument rects
    sound_rect = []
    for i in range(sounds):
        rect = pygame.rect.Rect((0, 100*i), (200, 100))
        sound_rect.append(rect)

    #save and load
    save = pygame.draw.rect(screen, grey, [900, height-150, 200, 48], 0, 5)
    save_text = label_font.render('Save', True, white)
    screen.blit(save_text, (920, height-140))
    Load = pygame.draw.rect(screen, grey, [900, height-100, 200, 48], 0, 5)
    Load_text = label_font.render('Load', True, white)
    screen.blit(Load_text, (920, height-90))

    # clear board
    clear = pygame.draw.rect(screen, grey, [1150, height-150, 200, 100], 0, 5)
    clear_text = label_font.render('Clear board', True, white)
    screen.blit(clear_text, (1160, height-120))

    # save and load menus:
    if SaveMenu:
        exitButton, savingButton, entry_rectangle = draw_SaveMenu(
            beat_name, typing)
    if LoadMenu:
        exitButton, loadingButton, entry_rectangle, deleteButton, loadInfo = draw_LoadMenu(
            index)

    if beatChanged:
        play_note()
        beatChanged = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
        if event.type == pygame.MOUSEBUTTONDOWN and not SaveMenu and not LoadMenu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1

        if event.type == pygame.MOUSEBUTTONUP and not SaveMenu and not LoadMenu:
            if playPause.collidepoint(event.pos):
                if Playing:
                    Playing = False
                elif not Playing:
                    Playing = True
            if bpmUp.collidepoint(event.pos):
                bpm = bpm + 5
            if bpmDown.collidepoint(event.pos):
                bpm = bpm - 5
            if beatsDown.collidepoint(event.pos):
                beats = beats - 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            if beatsUp.collidepoint(event.pos):
                beats = beats + 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            if clear.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(sounds)]
            if save.collidepoint(event.pos):
                SaveMenu = True
            if Load.collidepoint(event.pos):
                LoadMenu = True
            for i in range(len(sound_rect)):
                if sound_rect[i].collidepoint(event.pos):
                    activeList[i] *= -1
        elif event.type == pygame.MOUSEBUTTONUP:
            if exitButton.collidepoint(event.pos):
                SaveMenu = False
                LoadMenu = False
                Playing = True
                beat_name = ''
                typing = False
            if entry_rectangle.collidepoint(event.pos):
                if SaveMenu:
                    if typing:
                        typing = False
                    elif not typing:
                        typing = True
                if LoadMenu:
                    # if loadedRect.collidepoint(event.pos):
                    index = (event.pos[1] - 100) // 50
            if LoadMenu:
                if deleteButton.collidepoint(event.pos):
                    if 0 <= index < len(savedBeats):
                        savedBeats.pop(index)
                elif loadingButton.collidepoint(event.pos):
                    if 0 <= index < len(savedBeats):
                        beats = loadInfo[0]
                        bpm = loadInfo[1]
                        clicked = loadInfo[2]
                        LoadMenu = False
            if SaveMenu:
                if savingButton.collidepoint(event.pos):
                    file = open('SavedBeats.txt', 'w')
                    savedBeats.append(
                        f'\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}')
                    for i in range(len(savedBeats)):
                        file.write(str(savedBeats[i]))
                    file.close
                    SaveMenu = False
                    beat_name = ''

        if event.type == pygame.TEXTINPUT and typing:
            beat_name += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and len(beat_name) > 0 and typing:
                beat_name = beat_name[:-1]

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
