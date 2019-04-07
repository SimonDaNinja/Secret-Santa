import os
from copy import deepcopy
import random

def PrintAdjacencyMatrix(adjacencyMatrix):
    size = len(adjacencyMatrix)
    printString = ""
    for i in range(size):
        for j in range(size):
            if adjacencyMatrix[i][j]:
                printString += str(1) + " "
            else:
                printString += str(0) + " "
        printString += "\n"
    print(printString)

def AddNameToIncompatibilitySetDict(incompatibilitySetDict, nameSet, name):
    nameSet.add(name)
    incompatibilitySet = set()
    incompatibilitySet.add(name)
    while True:
        yn = input('\ndo you want to enter the name of someone that {} should NOT buy a present for? [y/n] '.format(name)).lower()
        if yn == 'y':
            incompatibleName = input('enter the name of someone that {} should NOT buy a present for: '.format(name))
            incompatibilitySet.add(incompatibleName) 
        elif yn == 'n':
            break
        else:
            print('invalid response!')
    incompatibilitySetDict[name] = incompatibilitySet
    while True:
        unaddedNames = incompatibilitySet-nameSet
        if unaddedNames:
            name = list(unaddedNames)[0]
            AddNameToIncompatibilitySetDict(incompatibilitySetDict, nameSet, name)
        else:
            break

if __name__ == '__main__':
    os.system('del /Q secret-santa-filer *.txt')
    # nameSet = {'andrea', 'aladdin', 'isabelle', 'pauline', 'simon', 'thomas'}

    nameSet = set()
    incompatibilitySetDict = dict()
    
    enteringNames = True
    while enteringNames:
        name = input('\nEnter the name of someone who is part of the secret santa session: ')
        AddNameToIncompatibilitySetDict(incompatibilitySetDict, nameSet, name)
        while True:
            yn = input('\ndo you want to add someone else to the secret santa session? [y/n] ').lower()
            if yn == 'y':
                break
            elif yn == 'n':
                enteringNames = False
                break
            else:
                print('invalid response!')


    while True:
        yn = input('\ndo you want to display the resulting secret santa list on screen?  [y/n] ').lower()
        if yn =='y':
            printOutSantaList = True
            break
        elif yn == 'n':
            printOutSantaList = False
            break
        else:
            print('invalid response')

    numberOfNames = len(nameSet)

    # nameNumberMap maps every name to an indexing number and vice versa
    nameNumberMap = dict()
    i = 0
    for name in nameSet:
        nameNumberMap[i] = name
        nameNumberMap[name] = i
        i +=1

    # here, we define the compatibility matrix
    compatibilityMatrix = [[True for i in range(numberOfNames)] for j in range(numberOfNames)]
    for giverIndex in range(numberOfNames):
        giverName = nameNumberMap[giverIndex]
        incompatibilitySet = incompatibilitySetDict[giverName]
        for receiverName in incompatibilitySet:
            receiverIndex = nameNumberMap[receiverName]
            compatibilityMatrix[giverIndex][receiverIndex] = False
    # here, we define the compatibility matrix
    # nobody can give to themselves
    # compatibilityMatrix = [[True for i in range(numberOfNames)] for j in range(numberOfNames)]
    # # Andrea can give to anyone except Thomas
    # compatibilityMatrix[nameNumberMap['andrea']][nameNumberMap['andrea']] = False
    # compatibilityMatrix[nameNumberMap['andrea']][nameNumberMap['thomas']] = False
    # # Aladdin can give to anyone except Isabelle
    # compatibilityMatrix[nameNumberMap['aladdin']][nameNumberMap['aladdin']] = False
    # compatibilityMatrix[nameNumberMap['aladdin']][nameNumberMap['isabelle']] = False
    # # Isabelle can give to anyone except Aladdin
    # compatibilityMatrix[nameNumberMap['isabelle']][nameNumberMap['isabelle']] = False
    # compatibilityMatrix[nameNumberMap['isabelle']][nameNumberMap['aladdin']] = False
    # compatibilityMatrix[nameNumberMap['isabelle']][nameNumberMap['pauline']] = False
    # # Pauline can give to anyone except Simon
    # compatibilityMatrix[nameNumberMap['pauline']][nameNumberMap['pauline']] = False
    # compatibilityMatrix[nameNumberMap['pauline']][nameNumberMap['simon']] = False
    # compatibilityMatrix[nameNumberMap['pauline']][nameNumberMap['isabelle']] = False
    # # Simon can give to anyone except Pauline
    # compatibilityMatrix[nameNumberMap['simon']][nameNumberMap['simon']] = False
    # compatibilityMatrix[nameNumberMap['simon']][nameNumberMap['pauline']] = False
    # # Thomas can give to anyone except Andrea
    # compatibilityMatrix[nameNumberMap['thomas']][nameNumberMap['thomas']] = False
    # compatibilityMatrix[nameNumberMap['thomas']][nameNumberMap['andrea']] = False

    # Here, we define the gift matrix
    while True:
        giftMatrix = [[False for i in range(numberOfNames)] for j in range(numberOfNames)]
        remainingCompatibilityMatrix = deepcopy(compatibilityMatrix)
        giftDict = dict()
        tryAgain = False
        for i in range(numberOfNames):
            # Choose for the giver with fewest compatible receivers
            compatibilityVectorLengths = []
            for j in range(numberOfNames):
                compatibilityVectorLength = 0
                compatibilityVector = remainingCompatibilityMatrix[j]
                for k in range(numberOfNames):
                    if compatibilityVector[k]:
                        compatibilityVectorLength += 1
                if compatibilityVectorLength > 0:
                    compatibilityVectorLengths.append(compatibilityVectorLength)
                else:
                    compatibilityVectorLengths.append(float('Inf'))
            giverIndex = compatibilityVectorLengths.index(min(compatibilityVectorLengths))
            giverCompatibilityVector = remainingCompatibilityMatrix[giverIndex]
            compatibleIndeces = [i for (i,x) in enumerate(giverCompatibilityVector) if x] 
            # If there are compatible receivers, choose one at random
            if len(compatibleIndeces)>0:
                receiverIndex = random.choice(compatibleIndeces)
            # Else, abort and tell the user the details of failure
            else:
                print("No compatible receivers remaining!")
                print("this is the original compatibility matrix:")
                PrintAdjacencyMatrix(compatibilityMatrix)
                print("This is the remaining compatibility matrix:")
                PrintAdjacencyMatrix(remainingCompatibilityMatrix)
                print("This is the current gift matrix:")
                PrintAdjacencyMatrix(giftMatrix)
                while True:
                    yn = input("Do you want to try again with the same names and incompatibilities? [y/n]").lower()
                    if yn == 'y':
                        tryAgain = True
                        break
                    elif yn =='n':
                        exit()
                    else:
                        print('invalid response!')
            if not tryAgain:
                # Modify the gift matrix accordingly
                giftMatrix[giverIndex][receiverIndex] = True
                # Modify the gift dict accordingly
                giverName = nameNumberMap[giverIndex]
                receiverName = nameNumberMap[receiverIndex]
                giftDict[giverName] = receiverName
                # Modify the remaining compatibility matrix
                for j in range(numberOfNames):
                    remainingCompatibilityMatrix[j][receiverIndex] = False 
                for j in range(numberOfNames):
                    remainingCompatibilityMatrix[giverIndex][j] = False 
            else:
                break
        if not tryAgain:
            break
    print(' ')
    for giver in giftDict:
        if printOutSantaList:
            print("{} should buy {} a gift".format(giver, giftDict[giver]))
        fileName = "secret-santa-filer/" + giver + ".txt"
        fileVar = open(fileName,'w')
        fileVar.write(giftDict[giver])
