def draw_SaveMenu():
    exitBtn = pygame.draw.rect(screen, grey, [width-200, height-100, 180, 90], 0, 5)
    exitText = label_font.render('Close', True, white)
    screen.blit(exitText, (width-160, height-70))
    return exitBtn