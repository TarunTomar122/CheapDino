import pygame

WIDTH = 600
HEIGHT = 400
FPS = 30
TOTALPLAYERS = 10
FPSCLOCK = 30

IMAGES = {}

def main():
    global FPSCLOCK,SCREEN,IMAGES

    pygame.init()
    pygame.display.set_caption('Dino Hack')



    SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
    FPSCLOCK = pygame.time.Clock()

    IMAGES['cactus'] = pygame.image.load('./cactus.png')
    IMAGES['player'] = pygame.image.load('./player.png')

    while True:
        playGame()

def playGame():
    global FPSCLOCK,SCREEN

    running = True

    cacShift = -4

    playerVel = []
    playerDownAcc = 4
    playerUpVel = -5

    for player in range(TOTALPLAYERS):
        playerVel.append(HEIGHT-IMAGES['player'].get_height())

    cactus = [
        {'x':WIDTH//2, 'y':HEIGHT-IMAGES['cactus'].get_height()},
        {'x':WIDTH, 'y':HEIGHT-IMAGES['cactus'].get_height()}
    ]

    while running:

        SCREEN.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                for player in range(TOTALPLAYERS):
                    playerVel[player] = playerUpVel

        for player in range(TOTALPLAYERS):
            if playerVel[player]>HEIGHT-IMAGES['player'].get_height():
                playerVel[player] += playerDownAcc

        for player in range(TOTALPLAYERS):
            SCREEN.blit(IMAGES['player'],(0,playerVel[player]))

        for cac in cactus:
            cac['x'] += cacShift 

        if cactus[0]['x']<=0:
            cactus.append({'x':WIDTH, 'y':HEIGHT-IMAGES['cactus'].get_height()})
            cactus.pop(0)

        for cac in cactus:
            SCREEN.blit(IMAGES['cactus'],(cac['x'],cac['y']))   

        pygame.display.update()
        FPSCLOCK.tick(FPS)   

main()        