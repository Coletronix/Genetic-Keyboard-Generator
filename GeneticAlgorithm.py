import random
from KeyboardAgent import KeyboardAgent, precalculateKeyDistances
import json
import pygame
import os
import math
import regex as re

# General genetic algorithm class
class GeneticAlgorithm:
    def __init__(self, populationSize, mutationRate, elitismCount, trainingData=''):
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.elitismCount = elitismCount
        self.currentGeneration = 0
        self.bestAgent = None
        self.previousBestFitness = 0
        self.population = []
        precalculateKeyDistances(KeyboardAgent(False, trainingData))
        for _ in range(populationSize):
            test = KeyboardAgent(False, trainingData)
            self.population.append(test)
            
    def evolveOneGeneration(self):
        newPopulation = []
        
        for agent in self.population:
            agent.calculateFitness()
        
        self.population.sort(reverse=True)
        
        self.bestAgent = self.population[0]
        
        elites = self.population[:self.elitismCount]
        
        for i in range(self.elitismCount, self.populationSize):
            parent1 = random.choice(self.population)
            parent2 = random.choice(self.population)
            
            child = parent1.crossover(parent2)
            
            newPopulation.append(child)

        # the mutation rate should increase if the best agent is not improving, and decrease if it is
        # maximum mutation rate is 0.1
        if self.bestAgent.fitness > self.previousBestFitness and self.mutationRate > minMutationRate:
            self.mutationRate *= 0.7
        elif self.mutationRate < maxMutationRate:
            self.mutationRate *= 1.1
        self.previousBestFitness = self.bestAgent.fitness

        # mutate new population (except elites)
        for agent in newPopulation:
            if random.random() < self.mutationRate:
                agent.mutate(random.random() * self.mutationRate)
        
        newPopulation = newPopulation + elites
        
        
        self.population = newPopulation
        self.currentGeneration += 1
        
    def getBestAgent(self):
        return self.bestAgent
    
    def setTrainingData(self, trainingData):
        for agent in self.population:
            agent.trainingData = trainingData
    
def loadFile(filename):
    with open(filename, 'r') as f:
        return f.read()    

def loadFolder(folder):
    files = os.listdir(folder)
    data = []
    for file in files:
        data.append(loadFile(folder + '/' + file))
    return data

# paramters
# trainingDataFolder = 'trainingTextsLarge'
trainingDataFolder = 'trainingTextSuperLarge'
tournamentSize = 10000
generationSize = 100
swapTrainingDataEvery = 40000
initialMutationRate = 0.01
maxMutationRate = 0.2
minMutationRate = 0.0001

def main():
    trainingDataOptions = loadFolder(trainingDataFolder)

    trainingData = random.choice(trainingDataOptions)
    trainingData = trainingData.lower()
    # remove all characters according to a regex everything that is not a-z or a space or a slash
    trainingData = re.sub("[^a-z /.,';]", '', trainingData)
    trainingDataLength = len(trainingData)
    print("Training data new length: " + str(trainingDataLength))

    pygame.init()
    font = pygame.font.SysFont('Arial', 30)
    screen = pygame.display.set_mode((590, 150))
    clock = pygame.time.Clock()
    
    ga = GeneticAlgorithm(generationSize, initialMutationRate, 3, trainingData=trainingData)
    qwerty = KeyboardAgent(True, trainingData=trainingData)
    dvorak = KeyboardAgent(True, trainingData=trainingData)
    workman = KeyboardAgent(True, trainingData=trainingData)
    special = KeyboardAgent(True, trainingData=trainingData)
    qwerty.keymap = json.loads(loadFile("keyboardLayouts/qwertyLayout.json"))
    dvorak.keymap = json.loads(loadFile("keyboardLayouts/dvorakLayout.json"))
    workman.keymap = json.loads(loadFile("keyboardLayouts/workmanLayout.json"))
    special.keymap = json.loads(loadFile("keyboardLayouts/layoutChoice1.json"))
    qwerty.calculateFitness()
    dvorak.calculateFitness()
    workman.calculateFitness()
    special.calculateFitness()
    
    numTimesEachKeyPressedBest = qwerty.getNumTimesEachKeyPressed()
    maxNumTimesKeyPressed = max(numTimesEachKeyPressedBest.values())
    
    stopAlgorithm = False
    
    for i in range(tournamentSize):
        if i % swapTrainingDataEvery == 0:
            trainingData = random.choice(trainingDataOptions)
            trainingData = trainingData.lower()
            trainingDataLength = len(trainingData)
            print("Training data new length: " + str(trainingDataLength))
            print("Selected training data: " + trainingData[:50])
            ga.setTrainingData(trainingData)
        
        ga.evolveOneGeneration()
        #print("CurrentMutationRate: " + str(ga.mutationRate))
        #print("Generation:", ga.currentGeneration, "Best Fitness:", ga.getBestAgent().fitness, "Mutation Rate:", ga.mutationRate)


        screen.fill((0, 0, 0))
        pygame.display.set_caption("Gen: " + str(ga.currentGeneration) + "Fitness: " + str(ga.getBestAgent().fitness))

        
        keySize = 50
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stopAlgorithm = True
            # user hit save
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                with open("keyboardLayouts/bestKeyboardLayout.json", 'w') as f:
                    f.write(json.dumps(ga.getBestAgent().keymap))
        
        for (key, position) in ga.getBestAgent().keymap.items():
            heatValue = 255 * numTimesEachKeyPressedBest[key]/maxNumTimesKeyPressed # from 0 to 255
            color = (heatValue, .5 * (255-heatValue), 0)
            rect = pygame.Rect(position[0] * keySize, position[1] * keySize, keySize, keySize)
            pygame.draw.rect(screen, color, rect)
            # text of each key on top of each rect
            text = font.render(key.upper(), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))
        
        pygame.display.flip()
        
        if stopAlgorithm:
            break
    
    # test the efficiency of some known layouts
    print("QWERTY Fitness:", qwerty.fitness, "Back and Forthness:", qwerty.getBackAndForthness(), "Finger Usage: ", qwerty.getNumTimesEachFingerUsed())
    print("Dvorak Fitness:", dvorak.fitness, "Back and Forthness:", dvorak.getBackAndForthness(), "Finger Usage: ", dvorak.getNumTimesEachFingerUsed())
    print("Workman Fitness:", workman.fitness, "Back and Forthness:", workman.getBackAndForthness(), "Finger Usage: ", workman.getNumTimesEachFingerUsed())
    print("Special Fitness:", special.fitness, "Back and Forthness:", special.getBackAndForthness(), "Finger Usage: ", special.getNumTimesEachFingerUsed())
    print("Best Fitness:", ga.getBestAgent().fitness, "Back and Forthness:", ga.getBestAgent().getBackAndForthness(), "Finger Usage: ", ga.getBestAgent().getNumTimesEachFingerUsed())
    
    # show the best agent with pygame
    chosenAgent = ga.getBestAgent()
    # chosenAgent = qwerty
    # chosenAgent = dvorak
    # chosenAgent = special
    trainingDataLetterIndex = 0 # for animation
    numTimesEachKeyPressedBest = chosenAgent.getNumTimesEachKeyPressed()
    maxNumTimesKeyPressed = max(numTimesEachKeyPressedBest.values())
    showHeatmap = False
    while True:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            # user hit save
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    with open("keyboardLayouts/bestKeyboardLayout.json", 'w') as f:
                        f.write(json.dumps(chosenAgent.keymap))
                # user hit show heatmap
                if event.key == pygame.K_h:
                    showHeatmap = not showHeatmap
        screen.fill((0, 0, 0))
        
        keySize = 50
        font = pygame.font.SysFont('Arial', 30)
        for (key, position) in chosenAgent.keymap.items():
            if not showHeatmap:
                if key != trainingData[trainingDataLetterIndex]:
                    keyPos = chosenAgent.keymap[key]
                    fingerNumberRaw = math.floor(keyPos[0])
                    if (fingerNumberRaw == 4):
                        fingerNumberRaw -= 1
                    elif (fingerNumberRaw == 5):
                        fingerNumberRaw -= 1
                    elif (fingerNumberRaw >= 6):
                        fingerNumberRaw -= 2
                        
                    # pick color based on finger
                    if fingerNumberRaw == 0:
                        color = (255, 0, 0)
                    elif fingerNumberRaw == 1:
                        color = (0, 255, 0)
                    elif fingerNumberRaw == 2:
                        color = (0, 0, 255)
                    elif fingerNumberRaw == 3:
                        color = (255, 255, 0)
                    elif fingerNumberRaw == 4:
                        color = (255, 0, 255)
                    elif fingerNumberRaw == 5:
                        color = (0, 255, 255)
                    elif fingerNumberRaw == 6:
                        color = (255, 255, 255)
                    else:
                        color = (127, 127, 127)
                else:
                    color = (255, 255, 255)
            else:
                # show heatmap
                heatValue = 255 * numTimesEachKeyPressedBest[key]/maxNumTimesKeyPressed # from 0 to 255
                color = (heatValue, .5 * (255-heatValue), 0)
            rect = pygame.Rect(position[0] * keySize, position[1] * keySize, keySize, keySize)
            pygame.draw.rect(screen, color, rect)
            # text of each key on top of each rect
            text = font.render(key.upper(), True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))
        
        pygame.display.flip()
        trainingDataLetterIndex += 1
        if trainingDataLetterIndex >= len(trainingData):
            trainingDataLetterIndex = 0

if __name__ == '__main__':
    main()