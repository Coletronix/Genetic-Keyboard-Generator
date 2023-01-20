from bidict import bidict
import random
import GeneticAgent
import math

def swapKeyPos(keyA, keyB, dict):
    dict[keyA], dict[keyB] = dict[keyB], dict[keyA]

singleKeyFreqs = dict()
bigramFreqs = dict()
trigramFreqs = dict()
keyDistances = dict()

def precalculateKeyDistances(agent):
    global keyDistances
    for (keyA, posA) in agent.keymap.items():
        for (keyB, posB) in agent.keymap.items():
            keyDistances[(posA[0], posA[1], posB[0], posB[1])] = math.sqrt((posA[0] - posB[0]) ** 2 + (posA[1] - posB[1]) ** 2)

def precalculateSingleKeyFreqs(agent):
    global singleKeyFreqs
    for i in range(len(agent.trainingData)):
        key = agent.trainingData[i]
        if key == ' ':
            continue
        if key in singleKeyFreqs.keys():
            singleKeyFreqs[key] += 1
        else:
            singleKeyFreqs[key] = 1
    # normalize
    for key in singleKeyFreqs.keys():
        singleKeyFreqs[key] /= len(agent.trainingData)
        
def precalculateBigramFreqs(agent):
    global bigramFreqs
    bigramFreqsTemp = dict()
    for i in range(len(agent.trainingData) - 1):
        bigram = agent.trainingData[i:i+2]
        if bigram[0] == ' ' or bigram[1] == ' ':
            continue
        if bigram in bigramFreqsTemp.keys():
            bigramFreqsTemp[bigram] += 1
        else:
            bigramFreqsTemp[bigram] = 1
    # normalize
    for bigram in bigramFreqsTemp.keys():
        if bigramFreqsTemp[bigram] != 1:
            bigramFreqs[bigram] = bigramFreqsTemp[bigram] / (len(agent.trainingData) - 1)

def precalculateTrigramFreqs(agent):
    global trigramFreqs
    trigramFreqsTemp = dict()
    for i in range(len(agent.trainingData) - 2):
        trigram = agent.trainingData[i:i+3]
        if trigram[0] == ' ' or trigram[1] == ' ' or trigram[2] == ' ':
            continue
        if trigram in trigramFreqsTemp.keys():
            trigramFreqsTemp[trigram] += 1
        else:
            trigramFreqsTemp[trigram] = 1
    # normalize
    for trigram in trigramFreqsTemp.keys():
        if trigramFreqsTemp[trigram] != 1:
            trigramFreqs[trigram] = trigramFreqsTemp[trigram] / (len(agent.trainingData) - 2)

class KeyboardAgent:
    def __init__(self, empty=False, trainingData=''):
        # create a random keymapping.
        # keymap is stored in a dictionary, and relates key codes
        # with physical position on keyboard.
        
        self.keymap = {}
        self.trainingData = trainingData
        
        if not empty:
            if len(bigramFreqs.keys()) == 0:
                precalculateSingleKeyFreqs(self)
                precalculateBigramFreqs(self)
                precalculateTrigramFreqs(self)
                print(sorted(bigramFreqs.items(), key=lambda x: x[1], reverse=True))
            # begin with standard staggered qwerty layout
            self.keymap = {
                'q' : (0, 0),
                'w' : (1, 0),
                'e' : (2, 0),
                'r' : (3, 0),
                't' : (4, 0),
                'y' : (5, 0),
                'u' : (6, 0),
                'i' : (7, 0),
                'o' : (8, 0),
                'p' : (9, 0),
                'a' : (0.25, 1),
                's' : (1.25, 1),
                'd' : (2.25, 1),
                'f' : (3.25, 1),
                'g' : (4.25, 1),
                'h' : (5.25, 1),
                'j' : (6.25, 1),
                'k' : (7.25, 1),
                'l' : (8.25, 1),
                ';' : (9.25, 1),
                '\'': (10.25, 1),
                'z' : (0.75, 2),
                'x' : (1.75, 2),
                'c' : (2.75, 2),
                'v' : (3.75, 2),
                'b' : (4.75, 2),
                'n' : (5.75, 2),
                'm' : (6.75, 2),
                ',' : (7.75, 2),
                '.' : (8.75, 2),
                '/' : (9.75, 2)
            }
            
            # now randomize the keymap
            keysList = list(self.keymap.keys())
            for i in range(len(keysList)):
                keyA = keysList[i]
                keyB = keysList[random.randint(i, len(keysList) - 1)]
                swapKeyPos(keyA, keyB, self.keymap)
        
        self.fitness = 0.0
        
    def crossover(self, other):
        child = KeyboardAgent(empty=True, trainingData=self.trainingData)
        
        # crossover with another agent        
        dict1 = bidict(self.keymap)
        dict2 = bidict(other.keymap)
        child.keymap = dict(zip([key for key in dict2.keys()], [value for value in dict2.values()]))

        startingIndex = list(dict1.keys())[random.randint(0, len(dict1)-1)]
        currentIndex = startingIndex
        while True:
            child.keymap[currentIndex] = dict1[currentIndex]
            currentIndex = dict1.inverse[dict2[currentIndex]]
            
            if (currentIndex == startingIndex):
                break
        
        return child
    
    # '''
    # Calculate the fitness of this agent.
    # Emphasis is placed on having important keys in the homerow, alternating between hands, and having the most common keys in the most common positions.
    # It also focuses on key distance.
    # '''
    # def calculateFitness(self):
    #     self.fitness = 0.0
        
    #     previouslyRightHandKey = self.keymap[self.trainingData[0]][0] > 4.8
        
    #     fingerPositions = [[.25, 1],
    #                        [1.25,1],
    #                        [2.25,1],
    #                        [3.25,1],
    #                        [6.25,1],
    #                        [7.25,1],
    #                        [8.25,1],
    #                        [9.25,1],
    #                        ]
        
    #     pFingerNum = 0
    #     ppFingerNum = 0
        
    #     # special keys that I would like to be in the same place
    #     # if self.keymap['c'][0] != 2.75 or self.keymap['c'][1] != 2:
    #     #     return # force position of a
    #     # elif self.keymap['v'][0] != 3.75 or self.keymap['v'][1] != 2:
    #     #     self.fitness += 1
    #     #     return # force position of v
    #     # elif self.keymap['x'][0] != 1.75 or self.keymap['x'][1] != 2:
    #     #     self.fitness += 2
    #     #     return # force position of x
    #     # elif self.keymap['z'][0] != 0.75 or self.keymap['z'][1] != 2: 
    #     #     self.fitness += 3
    #     #     return # force position of z
    #     # elif self.keymap['a'][0] != 0.25 or self.keymap['a'][1] != 1:
    #     #     self.fitness += 4
    #     #     return # force position of a
    #     # else:
    #     #     self.fitness += 5
        
    #     for i in range(1, len(self.trainingData)):
    #         key = self.trainingData[i]
            
    #         ordBetween = (ord(key) >= 97 and ord(key) <= 122)
    #         if ordBetween or key == ',' or key == '.' or key == '/':                                
    #             # optimize keys to minimize distance
    #             keyPos = self.keymap[key]
    #             fingerNumber = math.floor(keyPos[0])
    #             if (fingerNumber == 4):
    #                 fingerNumber -= 1
    #             elif (fingerNumber == 5):
    #                 fingerNumber -= 1
    #             elif (fingerNumber >= 6):
    #                 fingerNumber -= 2
                
    #             previousFingerPos = fingerPositions[fingerNumber]
    #             # distance = (keyPos[0] - previousFingerPos[0])**2 + (keyPos[1] - previousFingerPos[1])**2
    #             distance = keyDistances[(keyPos[0], keyPos[1], previousFingerPos[0], previousFingerPos[1])]
    #             self.fitness += .5/distance if distance != 0 else 2
                
    #             # extra point if the key is in the home row, .5 if it is in the top row
    #             if (keyPos[1] == 1):
    #                 self.fitness += 1
    #             elif (keyPos[1] == 0):
    #                 self.fitness += .5
                    
    #             # more points for stronger fingers (index, middle, ring)
    #             if fingerNumber == 3 or fingerNumber == 4: # index
    #                 self.fitness += 1
    #             elif fingerNumber == 2 or fingerNumber == 5: # middle
    #                 self.fitness += .75
    #             elif fingerNumber == 1 or fingerNumber == 6: # ring
    #                 self.fitness += .5
                    
    #             # optimize back and forth between hands
    #             rightHandKey = self.keymap[key][0] > 4.8
    #             if (rightHandKey != previouslyRightHandKey):
    #                 self.fitness += 3
    #             else:
    #                 # optimize same hand finger order
    #                 # penalize if finger order is not in one direction (eg. 1,2,3, not 1,3,2)
    #                 if ppFingerNum != None:
    #                     if (pFingerNum < ppFingerNum and fingerNumber > pFingerNum) or (pFingerNum > ppFingerNum and fingerNumber < pFingerNum):
    #                         self.fitness -= 2 # penalize
    #                     else:
    #                         self.fitness += 1 # reward
    #                         # additional reward if the finger order going towards the center of the keyboard
    #                         if (pFingerNum == ppFingerNum+1 and fingerNumber == pFingerNum+1 and fingerNumber <= 3) or (pFingerNum == ppFingerNum-1 and fingerNumber == pFingerNum-1 and fingerNumber >= 4):
    #                             self.fitness += 1
                    
    #                     if (rightHandKey and fingerNumber == pFingerNum -1) or (not rightHandKey and fingerNumber == pFingerNum +1):
    #                         self.fitness += 1 # reward for going towards the center of the keyboard
                    
    #             # penalize a lot if the same finger is used twice in a row
    #             if (fingerNumber == pFingerNum):
    #                 self.fitness -= 10
                    
    #             # non alphabet keys should be on the right pinky
    #             # if not ordBetween:
    #             #     if fingerNumber == 7:
    #             #         self.fitness += 1
                        
    #             # penalize a small amount if in the middle column
    #             if keyPos[0] >= 4 and keyPos[0] < 6:
    #                 self.fitness -= .5
                        
    #             previouslyRightHandKey = rightHandKey
    #             fingerPositions[fingerNumber] = keyPos
    #             ppFingerNum = pFingerNum
    #             pFingerNum = fingerNumber
    
    '''
    Calculate the fitness of this agent.
    Emphasis is placed on having movements that are not pointy. (no sharp angles between 3 keys)
    '''
    # def calculateFitness(self):
    #     self.fitness = 0
        
    #     ppKey = self.trainingData[0]
    #     pKey = self.trainingData[1]
    #     for i in range(2, len(self.trainingData)):
    #         key = self.trainingData[i]
            
    #         ordBetween = (ord(key) >= 97 and ord(key) <= 122)
    #         if ordBetween or key == ',' or key == '.' or key == '/':                
                
    #             # calculate angle between 3 keys
    #             ppKeyPos = self.keymap[ppKey]
    #             pKeyPos = self.keymap[pKey]
    #             keyPos = self.keymap[key]
                
    #             self.fitness += math.fabs(math.atan2(ppKeyPos[1]-pKeyPos[1], ppKeyPos[0]-pKeyPos[0]) - math.atan2(keyPos[1]-pKeyPos[1], keyPos[0]-pKeyPos[0]))

    #             dist = math.sqrt((ppKeyPos[0]-pKeyPos[0])**2 + (ppKeyPos[1]-pKeyPos[1])**2) + math.sqrt((keyPos[0]-pKeyPos[0])**2 + (keyPos[1]-pKeyPos[1])**2)
    #             self.fitness += 1/dist if dist != 0 else 1
                
    #             # extra point if the key is in the home row, .5 if it is in the top row
    #             if (keyPos[1] == 1):
    #                 self.fitness += 1
    #             elif (keyPos[1] == 0):
    #                 self.fitness += .5
                
    #             ppKey = pKey
    #             pKey = key
    
    '''
    Calculate the fitness of this agent.
    Emphasis is placed using the two pointer fingers centered over f and j
    '''
    # def calculateFitness(self):
    #     self.fitness = 0
        
    #     for i in range(2, len(self.trainingData)):
    #         key = self.trainingData[i]
            
    #         ordBetween = (ord(key) >= 97 and ord(key) <= 122)
    #         if ordBetween or key == ',' or key == '.' or key == '/':                
                
    #             keyPos = self.keymap[key]
                
    #             d = ((keyPos[0] - 3.25)**2 + (keyPos[1] - 1)**2)
    #             self.fitness += 1/d if d != 0 else 1
    #             d = ((keyPos[0] - 6.25)**2 + (keyPos[1] - 1)**2)
    #             self.fitness += 1/d if d != 0 else 1
    
    '''
    Calculate the fitness of this agent.
    Emphasis is placed calculating how physically long it would take to go from one key to the next.
    '''
    # def calculateFitness(self):
    #     self.fitness = 0
        
    #     pKey = self.trainingData[1]
    #     for i in range(2, len(self.trainingData)):
    #         key = self.trainingData[i]
            
    #         ordBetween = (ord(key) >= 97 and ord(key) <= 122)
    #         if ordBetween or key == ',' or key == '.' or key == '/':                
                
                
                
    #             pKey = key
    
    '''
    Calculate the fitness of this agent.
    Emphasis is placed on having bigrams and trigrams in easy to type positions.
    '''
    def calculateFitness(self):
        self.fitness = 0.0
        singleKeyFitness = 0.0
        bigramFitness = 0.0
        trigramFitness = 0.0
        for (key, frequency) in singleKeyFreqs.items():
            keyPos = self.keymap[key]
            fingerNumber = math.floor(keyPos[0])
            if (fingerNumber == 4):
                fingerNumber -= 1
            elif (fingerNumber == 5):
                fingerNumber -= 1
            elif (fingerNumber >= 6):
                fingerNumber -= 2
            fingerNumber = min(fingerNumber, 7)
            
            # extra point if the key is in the home row, .5 if it is in the top row
            if (keyPos[1] == 1):
                singleKeyFitness += frequency
            elif (keyPos[1] == 0):
                singleKeyFitness += frequency / 2.0
                
            # more points for stronger fingers (index, middle, ring)
            if fingerNumber == 3 or fingerNumber == 4: # index
                singleKeyFitness += frequency * 0.5
            elif fingerNumber == 2 or fingerNumber == 5: # middle
                singleKeyFitness += 0.75 * frequency * 0.5
            elif fingerNumber == 1 or fingerNumber == 6: # ring
                singleKeyFitness += 0.5 * frequency * 0.5
                
            # penalize for using the center column
            if keyPos[0] >= 4 and keyPos[0] < 6:
                singleKeyFitness -= .5 * frequency * .5
                
        for (bigram, frequency) in bigramFreqs.items():
            key1Pos = self.keymap[bigram[0]]
            key2Pos = self.keymap[bigram[1]]
            fingerNumber1 = math.floor(key1Pos[0])
            if (fingerNumber1 == 4):
                fingerNumber1 -= 1
            elif (fingerNumber1 == 5):
                fingerNumber1 -= 1
            elif (fingerNumber1 >= 6):
                fingerNumber1 -= 2
            fingerNumber1 = min(fingerNumber1, 7)
            fingerNumber2 = math.floor(key2Pos[0])
            if (fingerNumber2 == 4):
                fingerNumber2 -= 1
            elif (fingerNumber2 == 5):
                fingerNumber2 -= 1
            elif (fingerNumber2 >= 6):
                fingerNumber2 -= 2
            fingerNumber2 = min(fingerNumber2, 7)
            
            # check if they are on opposite sides of the keyboard
            if (fingerNumber1 >= 4 and fingerNumber2 <= 4) or (fingerNumber1 <= 3 and fingerNumber2 >= 4):
                bigramFitness += frequency
            else:
                # same row, fingers one off, and going towards the center
                if fingerNumber1 == fingerNumber2: # same finger
                    bigramFitness -= frequency * 5
                else:
                    # check which hand it is on
                    if fingerNumber1 <= 3: # left
                        if key1Pos[1] == key2Pos[1]:
                            if fingerNumber2 == fingerNumber1 + 1:
                                bigramFitness += frequency
                            elif fingerNumber2 == fingerNumber1 - 1:
                                bigramFitness += frequency * .5 # still good if they are in order, just less so
                    else: # right
                        if key1Pos[1] == key2Pos[1]:
                            if fingerNumber2 == fingerNumber1 - 1:
                                bigramFitness += frequency
                            elif fingerNumber2 == fingerNumber1 + 1:
                                bigramFitness += frequency * .5 # still good if they are in order, just less so
            
        for (trigram, frequency) in trigramFreqs.items():
            key1Pos = self.keymap[trigram[0]]
            key2Pos = self.keymap[trigram[1]]
            key3Pos = self.keymap[trigram[2]]
            fingerNumber1 = math.floor(key1Pos[0])
            if (fingerNumber1 == 4):
                fingerNumber1 -= 1
            elif (fingerNumber1 == 5):
                fingerNumber1 -= 1
            elif (fingerNumber1 >= 6):
                fingerNumber1 -= 2
            fingerNumber1 = min(fingerNumber1, 7)
            fingerNumber2 = math.floor(key2Pos[0])
            if (fingerNumber2 == 4):
                fingerNumber2 -= 1
            elif (fingerNumber2 == 5):
                fingerNumber2 -= 1
            elif (fingerNumber2 >= 6):
                fingerNumber2 -= 2
            fingerNumber2 = min(fingerNumber2, 7)
            fingerNumber3 = math.floor(key3Pos[0])
            if (fingerNumber3 == 4):
                fingerNumber3 -= 1
            elif (fingerNumber3 == 5):
                fingerNumber3 -= 1
            elif (fingerNumber3 >= 6):
                fingerNumber3 -= 2
            fingerNumber3 = min(fingerNumber3, 7)
            
            if fingerNumber1 <= 3: # left hand rolls
                if (fingerNumber2 == fingerNumber1 + 1) and (fingerNumber3 == fingerNumber2 + 1):
                    trigramFitness += frequency
                elif (fingerNumber2 == fingerNumber1 - 1) and (fingerNumber3 == fingerNumber2 - 1):
                    trigramFitness += frequency * .5 # still good if they are in order, just less so
            else: # right hand start
                if (fingerNumber2 == fingerNumber1 - 1) and (fingerNumber3 == fingerNumber2 - 1):
                    trigramFitness += frequency
                elif (fingerNumber2 == fingerNumber1 + 1) and (fingerNumber3 == fingerNumber2 + 1):
                    trigramFitness += frequency * .5 # still good if they are in order, just less so
                
            
        
        self.fitness = 0.5 * singleKeyFitness + 0.4 * bigramFitness + 0.1 * trigramFitness
        self.fitness *= 100.0 # to make it a percentage

    
    def mutate(self, mutationRate):
        for(key, value) in self.keymap.items():
            if (random.random() < mutationRate):
                swapKeyPos(key, list(self.keymap.keys())[random.randint(0, len(self.keymap)-1)], self.keymap)
    
    def getNumTimesEachFingerUsed(self):
        numTimesEachFingerUsed = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(0, len(self.trainingData)):
            key = self.trainingData[i]
            ordBetween = (ord(key) >= 97 and ord(key) <= 122)
            if ordBetween or key == ',' or key == '.' or key == '/':
                keyPos = self.keymap[key]
                fingerNumber = math.floor(keyPos[0])
                if (fingerNumber == 4):
                    fingerNumber -= 1
                elif (fingerNumber == 5):
                    fingerNumber -= 1
                elif (fingerNumber >= 6):
                    fingerNumber -= 2
                    
                numTimesEachFingerUsed[fingerNumber] += 1
        
        return numTimesEachFingerUsed
    
    def getNumTimesEachKeyPressed(self):
        numTimesEachKeyPressed = dict()
        for (key, value) in self.keymap.items():
            numTimesEachKeyPressed[key] = 0
        for i in range(0, len(self.trainingData)):
            key = self.trainingData[i]
            ordBetween = (ord(key) >= 97 and ord(key) <= 122)
            if ordBetween or key == ',' or key == '.' or key == '/':
                if key in numTimesEachKeyPressed:
                    numTimesEachKeyPressed[key] += 1
                else:
                    numTimesEachKeyPressed[key] = 1
        return numTimesEachKeyPressed
    
    def getBackAndForthness(self):
        previouslyRightHandKey = False
        alternationCount = 0
        for i in range(0, len(self.trainingData)):
            key = self.trainingData[i]
            ordBetween = (ord(key) >= 97 and ord(key) <= 122)
            if ordBetween or key == ',' or key == '.' or key == '/':
                rightHandKey = self.keymap[key][0] > 4.8
                if (rightHandKey != previouslyRightHandKey):
                    alternationCount += 1
                previouslyRightHandKey = rightHandKey
        
        return alternationCount/len(self.trainingData)
    
    def __lt__(self, other):
         return self.fitness < other.fitness # for sorting