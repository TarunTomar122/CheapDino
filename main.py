import pygame
import numpy as np
import random

from keras.models import Sequential
from keras.layers import Dense, Activation

TOTALPLAYERS = 20

WIDTH = 600
HEIGHT = 400
FPS = 30

FPSCLOCK = 30
MAXJUMP = 18

playerX = 50

IMAGES = {}

models = []
fitness = []

TOTALPARENTS = 5


for i in range(TOTALPLAYERS):
    model = Sequential()
    model.add(Dense(input_dim=2, units=1))
    model.add(Activation('sigmoid'))
    # model.add(Dense(units=1))
    # model.add(Activation('sigmoid'))

    fitness.append(0)
    models.append(model)


def predict(playerHeight, obstacleDistance, idx):
    global models

    playerHeight = playerHeight/HEIGHT
    obstacleDistance = obstacleDistance/WIDTH

    neuralInput = np.asarray([playerHeight, obstacleDistance])
    neuralInput = np.atleast_2d(neuralInput)

    output = models[idx].predict(neuralInput, 1)[0][0]

    if output <=0.5:
        return 1
    return 2    


def checkCollision(playerY, cactus):
    status = []
    for player in range(TOTALPLAYERS):
        status.append(False)
        for cac in range(len(cactus)):
            if cactus[cac]['x'] <= (playerX + 48) and playerY[player] >= HEIGHT - 128:
                status[player] = True
    return status

def nextGeneration():
    global models, fitness

    parents = []

    for parent in range(TOTALPARENTS):
        maxIdx = fitness.index(max(fitness))
        parents.append(models[maxIdx])
        fitness[maxIdx] = -1
    
    babiesWeights = []

    for baby in range(TOTALPLAYERS - TOTALPARENTS):
        kid = modelCrossover(models,baby%TOTALPARENTS,(baby+1)%TOTALPARENTS)
        kidMutated = modelMutate(kid)
        babiesWeights.append(kidMutated)

    for player in range(TOTALPARENTS):
        models[player] = parents[player]  

    for player in range(TOTALPARENTS,TOTALPLAYERS):
        models[player].set_weights(babiesWeights[player - TOTALPARENTS])      
        

def modelCrossover(current_pool,model_idx1, model_idx2):
    weights1 = current_pool[model_idx1].get_weights()
    weights2 = current_pool[model_idx2].get_weights()

    weightsnew = weights1

    weightsnew[0] = (weights2[0] + weights1[0])/2
    weightsnew[1] = (weights2[1] + weights1[1])/2

    return np.asarray(weightsnew)

def modelMutate(weights):
    for xi in range(len(weights)):
        for yi in range(len(weights[xi])):
            if random.uniform(0, 1) > 0.85:
                change = random.uniform(-0.5,0.5)
                weights[xi][yi] += change
    return weights              


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
        print("Total Fitness", sum(fitness))
        nextGeneration()


def playGame():
    global FPSCLOCK, SCREEN, TOTALPLAYERS, models, fitness

    for player in range(TOTALPLAYERS):
        fitness[player] = 0

    alivePlayers = TOTALPLAYERS

    running = True

    cacShift = -4

    playerYlist = []

    playerJump = []
    for player in range(TOTALPLAYERS):
        playerJump.append(-1-MAXJUMP)

    playerState = []

    for player in range(TOTALPLAYERS):
        playerYlist.append(HEIGHT-IMAGES['player'].get_height())
        playerState.append(True)

    cactus = [
        {'x': WIDTH//2, 'y': HEIGHT-IMAGES['cactus'].get_height()},
        {'x': WIDTH, 'y': HEIGHT-IMAGES['cactus'].get_height()}
    ]

    while running:

        SCREEN.fill((255, 255, 255))

        if alivePlayers == 0:
            return 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
        for player in range(TOTALPLAYERS):
            if predict(playerYlist[player],cactus[0]['x'], player) == 1 and playerState[player]:
                if playerJump[player] == (-MAXJUMP-1):
                    playerJump[player] = MAXJUMP

        status = checkCollision(playerYlist, cactus)

        for player in range(TOTALPLAYERS):
            if status[player] and playerState[player]:
                playerState[player] = False
                alivePlayers -= 1

        if alivePlayers == 0:
            return 

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

        for player in range(TOTALPLAYERS):
            if playerState[player]:
                fitness[player]+=1

        pygame.display.update()
        FPSCLOCK.tick(FPS)


main()
