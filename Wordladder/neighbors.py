#! /usr/bin/python3

import sys

def setupDict(inputFile, words):
    inputFile = open(inputFile,'r').read().split('\n')
    inputFile.pop()
    for i in inputFile:
        try:
            words[len(i)].append(i)
        except:
            words[len(i)] = [i]
    return words

words = {}
setupDict('dictall.txt',words)

neighbors = {}

def neighborsN(wordLen, wordDct, neighborsDict):
    tempDict = {}
    newDict = {}
    compsMade = 0
    if not(wordLen in words.keys()): return
    for i in wordDct[wordLen]:
        newDict[i] = []
        for j in range(wordLen):
            key = i[0:j] + "_" + i[j+1:]
            if not(key in tempDict.keys()):
                tempDict[key] = [i]
            else:
                tempDict[key].append(i)
    for i in wordDct[wordLen]:
        for j in range(wordLen):
            key = i[0:j] + "_" + i[j+1:]
            newDict[i].extend(tempDict[key])
        lst = []
        for j in range(len(newDict[i])-1,-1,-1):
            if newDict[i][j] != i: lst.append(newDict[i][j])
        newDict[i] = lst
    neighborsDict[wordLen] = newDict

def writeNeigh(inFile, outFile):
    inFile = open(inFile,'r').read().split('\n')
    outFile = open(outFile, 'w')
    for i in inFile:
        if not(len(i) in words.keys()): continue
        if not(i in words[len(i)]): continue
        if not(len(i) in neighbors.keys()):
            neighborsN(len(i), words, neighbors)
        #print(neighbors[len(i)][i])
        outFile.write(i + ',' + str( len(neighbors[len(i)][i]) ) + '\n')

#currTime = time.time()
writeNeigh(sys.argv[1],sys.argv[2])
#print(time.time()-currTime)
