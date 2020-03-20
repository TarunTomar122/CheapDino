import pygame

WIDTH = 600
HEIGHT = 400
FPS = 30
TOTALPLAYERS = 1
FPSCLOCK = 30
MAXJUMP = 18

playerX = 50

IMAGES = {}


def checkCollision(playerY, cactus):
    status = []
    for player in range(TOTALPLAYERS):
        status.append(False)
        for cac in range(len(cactus)):
            if cactus[cac]['x'] <= (playerX + 48) and playerY[player] >= HEIGHT - 128:
                status[player] = True
    return status


def main():
    global FPSCLOCK, SCREEN, IMAGES

    pygame.init()
    pygame.display.set_caption('Dino Hack')
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    FPSCLOCK = pygame.time.Clock()

    IMAGES['cactus'] = pygame.image.load('./cactus.png')
    IMAGES['player'] = pygame.image.load('./player.png')

    while True:
        playGame()
        print("New Generation")


def playGame():
    global FPSCLOCK, SCREEN, TOTALPLAYERS

    alivePlayers = TOTALPLAYERS

    running = True

    cacShift = -4

    playerYlist = []

    playerJump = []
    for player in range(TOTALPLAYERS):
        playerJump.append(-1-MAXJUMP)

    playerDownAcc = 4
    playerPress = -200
    playerState = []

    playerMinY = 200

    for player in range(TOTALPLAYERS):
        playerYlist.append(HEIGHT-IMAGES['player'].get_height())
        playerState.append(True)

    cactus = [
        {'x': WIDTH//2, 'y': HEIGHT-IMAGES['cactus'].get_height()},
        {'x': WIDTH, 'y': HEIGHT-IMAGES['cactus'].get_height()}
    ]

    while running:

        SCREEN.fill((255, 255, 255))

        status = checkCollision(playerYlist, cactus)

        for player in range(TOTALPLAYERS):
            if status[player]:
                playerState[player] = False
                alivePlayers -= 1

        if alivePlayers == 0:
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                for player in range(TOTALPLAYERS):
                    # if playerState[player] and playerYlist[player]>playerMinY:
                    #     playerYlist[player] += playerPress
                    if playerJump[player] == (-MAXJUMP-1):
                        playerJump[player] = MAXJUMP

        for player in range(TOTALPLAYERS):
            if playerState[player]:
                if playerJump[player] >= -MAXJUMP:
                    playerYlist[player] -= playerJump[player]
                    playerJump[player] -= 1

        for player in range(TOTALPLAYERS):
            if playerState[player]:
                SCREEN.blit(IMAGES['player'], (playerX, playerYlist[player]))

        for cac in cactus:
            cac['x'] += cacShift

        if cactus[0]['x'] <= 0:
            cactus.append({'x': WIDTH, 'y': HEIGHT -
                           IMAGES['cactus'].get_height()})
            cactus.pop(0)

        for cac in cactus:
            SCREEN.blit(IMAGES['cactus'], (cac['x'], cac['y']))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


main()
