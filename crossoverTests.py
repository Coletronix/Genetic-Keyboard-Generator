import random
from bidict import bidict

def func1(arr1, arr2):
    newArr = []
    used_set = dict()
    for i in range(len(arr1)):
        new = 0
        if random.random() < 0.5:
            new = arr1[i]
            if dict[new] == 1:
                new = arr2[i]
        else:
            new = arr2[i]
            if dict[new] == 1:
                new = arr1[i]
        newArr.append(new)
        used_set[new] = 1
    return newArr

def func2(arr1, arr2):
    newArr = []
    usedElements = dict()
    loopLen = len(arr1)
    i = 0
    itterations = 0
    while i < loopLen:
        if arr1[i] in usedElements: # arr1[i] is already used
            if(arr2[i] in usedElements): # arr2[i] is already used
                index1 = usedElements[arr1[i]][0]
                index2 = usedElements[arr2[i]][0]
                bottom = min(index1, index2)
                #print("Miss: " + str(i) + " -> " + str(bottom))
                # clear out used elements down to bottom
                for j in range(i-1, bottom, -1):
                    del usedElements[newArr[j]]
                
                index = newArr[bottom]
                choice = not usedElements[newArr[bottom]][1]
                del usedElements[newArr[bottom]]
                if choice:
                    selectedElement = arr1[bottom]
                else:
                    selectedElement = arr2[bottom]
                
                newArr = newArr[:bottom]
                i = bottom
            else:
                selectedElement = arr2[i]
        elif arr2[i] in usedElements: # arr2[i] is already used
            selectedElement = arr1[i]
        else:
            choice = random.random() < 0.5
            if choice:
                selectedElement = arr1[i]
            else:
                selectedElement = arr2[i]
        newArr.append(selectedElement)
        usedElements[selectedElement] = [i, choice]
        i += 1
        itterations += 1
    return newArr, itterations

def func3(arr1, arr2):
    newArr = []
    usedElements = dict()
    loopLen = len(arr1)
    i = 0
    itterations = 0
    while i < loopLen:
        alreadyFlipped = False
        if arr1[i] in usedElements: # arr1[i] is already used
            if(arr2[i] in usedElements): # arr2[i] is already used
                index1 = usedElements[arr1[i]][0]
                index2 = usedElements[arr2[i]][0]
                bottom = min(index1, index2)
                if usedElements[newArr[bottom]][2]: # we already flipped this one
                    bottom = max(index1, index2)
                    
                #print("Miss: " + str(i) + " -> " + str(bottom))
                # clear out used elements down to bottom
                for j in range(i-1, bottom, -1):
                    del usedElements[newArr[j]]
                
                index = newArr[bottom]
                choice = not usedElements[newArr[bottom]][1]
                del usedElements[newArr[bottom]]
                if choice:
                    selectedElement = arr1[bottom]
                else:
                    selectedElement = arr2[bottom]
                    
                alreadyFlipped = True
                
                newArr = newArr[:bottom]
                i = bottom
            else:
                selectedElement = arr2[i]
        elif arr2[i] in usedElements: # arr2[i] is already used
            selectedElement = arr1[i]
        else:
            choice = random.random() < 0.5
            if choice:
                selectedElement = arr1[i]
            else:
                selectedElement = arr2[i]
        newArr.append(selectedElement)
        usedElements[selectedElement] = [i, choice, alreadyFlipped]
        i += 1
        itterations += 1
    return newArr, itterations

def func4(arr1, arr2):
    newArr = [-1 for _ in range(len(arr1))]
    
    startingIndex = random.randint(0, len(arr1)-1)
    print(str(startingIndex), end=" ")
    firstNode = arr1[startingIndex]
    currentNode = arr2[firstNode]
    newArr[startingIndex] = firstNode
    while(currentNode != firstNode):
        newArr[currentNode] = currentNode
        currentNode = arr2[currentNode]
    # add everything else from arr2
    for i in range(len(arr2)):
        if newArr[i] == -1:
            newArr[i] = arr2[i]
    return newArr

def func5(arr1, arr2):
    newArr = arr2.copy()

    startingIndex = random.randint(0, len(arr1)-1)    
    #print(str(startingIndex))
    currentIndex = startingIndex
    while True:
        newArr[currentIndex] = arr1[currentIndex]
        currentIndex = arr1.index(arr2[currentIndex])
        
        if (currentIndex == startingIndex):
            break
    
    return newArr

def func6(dict1, dict2):
    newArr = dict(zip([key for key in dict2.keys()], [value for value in dict2.values()]))

    startingIndex = list(dict1.keys())[random.randint(0, len(dict1)-1)]
    currentIndex = startingIndex
    loopSize = 0
    while True:
        newArr[currentIndex] = dict1[currentIndex]
        currentIndex = dict1.inverse[dict2[currentIndex]]
        loopSize += 1
        
        if (currentIndex == startingIndex):
            break
    
    return newArr, startingIndex, loopSize

#random.seed(2)

thing1 = [chr(i) for i in range(ord('a'), ord('z')+1)]
thing2 = thing1.copy()
random.shuffle(thing2)
thing1 = bidict(zip([i for i in range(len(thing1))], thing1))
thing2 = bidict(zip([i for i in range(len(thing2))], thing2))

print("arr1: " + str(thing1))
print("arr2: " + str(thing2))

itterationsBetter = 0
for i in range(1000000):
    # result2, itterFunc2 = func2(thing1, thing2)
    # result3, itterFunc3 = func3(thing1, thing2)
    # print(str(result2), end='')
    # print((" unique     Itterations: " if result2 != thing1 and result2 != thing2 else " duplicate. Itterations: ") + str(itterFunc2), end=' ')
    # print(str(result3), end='')
    # print((" unique     Itterations: " if result3 != thing1 and result3 != thing2 else " duplicate. Itterations: ") + str(itterFunc3), end=' ')
    # if(itterFunc2 > itterFunc3):
    #     print("func3 is faster by " + str(itterFunc2 - itterFunc3))
    #     itterationsBetter += 1
    # elif(itterFunc2 < itterFunc3):
    #     print("func2 is faster by " + str(itterFunc3 - itterFunc2))
    #     itterationsBetter -= 1
    # else:
    #     print("same speed")
    result4, startingVar, loopSize = func6(thing1, thing2)
    if i % 10000 == 0:
        print("itteration " + str(i), end=' ')
        print(startingVar, loopSize, str(result4.values()))
    
    #print("      " + str(result4))

print("func3 is faster " + str(itterationsBetter) + " times")