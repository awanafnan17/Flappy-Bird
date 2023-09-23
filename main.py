import random
import sys
from turtle import width
import pygame
from pygame.locals  import *




fps = 32
screen_Width = 289
screen_Height = 511

window = pygame.display.set_mode((screen_Width, screen_Height))

ground_Y = screen_Height * 0.8
game_Sprites = {}
game_Sounds = {}
player = 'gallery/sprites/bird.png'
background = 'gallery/sprites/background.png'
pipe = 'gallery/sprites/pipe.png'

def welcome():
    player_X = int(screen_Width/5)
    player_Y = int((screen_Height - game_Sprites['player'].get_height())/2)
    message_X = int((screen_Width - game_Sprites['message'].get_width())/2)
    message_Y = int(screen_Height * 0.13)
    base_X = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_KP_ENTER):
                return
            else:
                window.blit(game_Sprites['background'], (0, 0))
                window.blit(game_Sprites['player'], (player_X, player_Y))
                window.blit(game_Sprites['message'], (message_X, message_Y))
                window.blit(game_Sprites['base'], (base_X, ground_Y))
                pygame.display.update()
                fpsClock.tick(fps)


def game():
    score = 0
    player_X = int(screen_Width/5)
    player_Y = int(screen_Width/2)
    base_X = 0

    newPipe1 = genPipe()
    newPipe2 = genPipe()

    upperPipes = [
        {'x': screen_Width + 200, 'y': newPipe1[0]['y']},
        {'x': screen_Width + 200 + (screen_Width/2), 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': screen_Width + 200, 'y': newPipe1[1]['y']},
        {'x': screen_Width + 200 + (screen_Width/2), 'y': newPipe2[1]['y']}
    ]

    pipeVel_X = -4
    playerVel_Y = -9
    playerMaxVel_Y = 10
    playerAcc_Y = 1
    flapAcc = -8
    playerFlapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_Y > 0:
                    playerVel_Y = flapAcc
                    playerFlapped = True
                    game_Sounds['wing'].play()


        crashTest = isCollide(player_X, player_Y, upperPipes, lowerPipes)

        if crashTest:
            return

        playerMidPos = player_X + game_Sprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + game_Sprites['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                # print(f"Your score is {score}")
                game_Sounds['point'].play()
        
        if playerVel_Y < playerMaxVel_Y and not playerFlapped:
            playerVel_Y += playerAcc_Y

        if playerFlapped:
            playerFlapped = False

        playerHeight = game_Sprites['player'].get_height()
        player_Y = player_Y + min(playerVel_Y, ground_Y - player_Y - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVel_X
            lowerPipe['x'] += pipeVel_X
        
        if 0<upperPipes[0]['x']<5:
            newpipe = genPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        if upperPipes[0]['x'] < -game_Sprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)


        window.blit(game_Sprites['background'], (0, 0))
        
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            window.blit(game_Sprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            window.blit(game_Sprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))



        window.blit(game_Sprites['pipe'][0], (upperPipe['x'], lowerPipe['y']))
        window.blit(game_Sprites['pipe'][1], (upperPipe['x'], lowerPipe['y']))
        window.blit(game_Sprites['base'], (base_X, ground_Y))
        window.blit(game_Sprites['player'], (player_X, player_Y))

        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digits in mydigits:
            width += game_Sprites['numbers'][digits].get_width()
        Xoffset = (screen_Width - width)/2

        for digits in mydigits:
            window.blit(game_Sprites['numbers'][digits], (Xoffset, screen_Height*.12))
            Xoffset += game_Sprites['numbers'][digits].get_width()

        pygame.display.update()
        fpsClock.tick(fps)


def isCollide(player_X, player_Y, upperPipes, lowerPipes):
    if player_Y>ground_Y - 25 or player_Y< 0:
        game_Sounds['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = game_Sprites['pipe'][0].get_height()
        if (player_Y < pipeHeight + pipe['y'] and abs(player_X - pipe['x']) < game_Sprites['pipe'][0].get_width()):
            game_Sounds['hit'].play()
            return True

    for pipe in lowerPipes:
        if (player_Y + game_Sprites['player'].get_height() > pipe['y']) and abs(player_X - pipe['x']) < game_Sprites['pipe'][0].get_width():
            game_Sounds['hit'].play()
            return True
    return False

def genPipe():
    pipeHeight = game_Sprites['pipe'][0].get_height()
    offset = screen_Height/3
    y2 = offset + random.randrange(0, int(screen_Height - game_Sprites['base'].get_height() - 1.2*offset))
    pipe_X = screen_Width + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipe_X, 'y': -y1},
        {'x': pipe_X, 'y': y2}
    ]
    return pipe




if __name__ == "__main__":
    pygame.init()
    fpsClock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    game_Sprites['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    game_Sprites['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    game_Sprites['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    game_Sprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )
    game_Sprites['background'] = pygame.image.load(background).convert()
    game_Sprites['player'] = pygame.image.load(player).convert_alpha()




    game_Sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    game_Sounds['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    game_Sounds['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    game_Sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    game_Sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')


    while True:
        welcome()
        game()