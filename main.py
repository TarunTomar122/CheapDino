import pygame
import numpy as np
import random

from keras.models import Sequential
from keras.layers import Dense, Activation

TOTALPLAYERS = 20
num_generations = 2000
WIDTH = 600
HEIGHT = 400
FPS = 1000

FPSCLOCK = 30
MAXJUMP = 18

playerX = 50

IMAGES = {}

models = []
fitness = []

TOTALPARENTS = 5


for i in range(TOTALPLAYERS):
    model = Sequential()
    model.add(Dense(input_dim=2, units=8))
    model.add(Activation('sigmoid'))
    model.add(Dense(units=1))
    model.add(Activation('sigmoid'))

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
    
    phitmask = getHitmask(IMAGES['player'])
    chitmask = getHitmask(IMAGES['cactus'])

    for player in range(TOTALPLAYERS):
        status.append(False)
        pRect = pygame.Rect(playerX,playerY[player],IMAGES['player'].get_width(),IMAGES['player'].get_height())
        for cac in range(len(cactus)):
            # if cactus[cac]['x'] <= (playerX + 16) and playerY[player] >= HEIGHT - 128:
            #     status[player] = True
            cRect = pygame.Rect(cactus[cac]['x'],cactus[cac]['y'],IMAGES['cactus'].get_width(),IMAGES['cactus'].get_height())

            if pixelCollision(pRect, cRect, phitmask, chitmask):
                status[player] = True
            
            
    return status


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

def nextGeneration():
    global models, fitness

    newWeights = []

    # parents = []

    # for parent in range(TOTALPARENTS):
    #     maxIdx = fitness.index(max(fitness))
    #     parents.append(models[maxIdx])
    #     fitness[maxIdx] = -1
    
    # babiesWeights = []

    # for baby in range(TOTALPLAYERS - TOTALPARENTS):
    #     kid = modelCrossover(models,baby%TOTALPARENTS,(baby+1)%TOTALPARENTS)
    #     kidMutated = modelMutate(kid)
    #     babiesWeights.append(kidMutated)

    # for player in range(TOTALPARENTS):
    #     models[player] = parents[player]  

    # for player in range(TOTALPARENTS,TOTALPLAYERS):
    #     models[player].set_weights(babiesWeights[player - TOTALPARENTS])    

    totalFitness = sum(fitness)

    for fit in range(TOTALPLAYERS):
        fitness[fit] /= totalFitness

    for player in range(TOTALPLAYERS//2):

        idx1 = -1
        idx2 = -1

        parent1 = random.uniform(0,1)
        parent2 = random.uniform(0,1)

        for idxx in range(TOTALPLAYERS):
            if fitness[idxx]>= parent1:
                idx1 = idxx

        for idxx in range(TOTALPLAYERS):
            if fitness[idxx]>= parent2:
                idx2 = idxx   

        weights = modelCrossover(models,idx1,idx2)
        
        weights1 = modelMutate(weights[0])
        weights2 = modelMutate(weights[1])

        newWeights.append(weights1)
        newWeights.append(weights2)

    for player in range(TOTALPLAYERS):
        models[player].set_weights(newWeights[player])

def modelCrossover(current_pool,model_idx1, model_idx2):
    weights1 = current_pool[model_idx1].get_weights()
    weights2 = current_pool[model_idx2].get_weights()

    # weightsnew = weights1

    # weightsnew[0] = (weights2[0] + weights1[0])/2
    # weightsnew[1] = (weights2[1] + weights1[1])/2

    weightsNew1 = weights1
    weightsNew2 = weights2 

    weights1[0] = weightsNew2[0]
    weights2[0] = weightsNew1[0]

    return np.asarray([weights1,weights2])

def modelMutate(weights):
    for xi in range(len(weights)):
        for yi in range(len(weights[xi])):
            # if random.uniform(0, 1) > 0.85:
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

    for generation in range(num_generations):
        playGame()
        print("max fitness in genaration[",generation,'] = ', max(fitness))
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
            if cactus[0]['x'] > playerX: xinp = cactus[0]['x']
            else: xinp = cactus[1]['x']
            if predict(playerYlist[player],xinp, player) == 1 and playerState[player]:
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
            cactus.append({'x': random.randint(WIDTH-100,WIDTH), 'y': HEIGHT -
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
