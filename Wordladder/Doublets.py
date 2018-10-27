#!/usr/bin/python3

# In[1]:


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
#writeNeigh(sys.argv[1],sys.argv[2])
#print(time.time()-currTime)


# In[2]:


class Pqueue(): #Array version

  def defaultComp(a,b):
    if a > b: return 1
    if a == b: return 0
    return -1

  def __init__(self, comparator = defaultComp):
    self.data = [None]
    self.comp = comparator

  def push(self,value):
    currIndex = len(self.data)
    self.data.append(value)
    while True: #Until parent is < input
      if currIndex == 1: break
      nextIndex = currIndex//2
      if self.comp(value, self.data[nextIndex]) == -1: #Swap with parent
        self.data[currIndex] = self.data[nextIndex]
        self.data[nextIndex] = value
        currIndex = nextIndex
      else: break
    return True

  def pop(self):
    if len(self.data) == 1: return None #Empty Queue
    output = self.data[1]
    if len(self.data) == 2: #Single Element Queue
        del self.data[1]
        return output
    self.data[1] = self.data.pop(len(self.data)-1) #Bring last value to the front
    currIndex = 1
    while True: #Swap previously last value with lesser child until both children are greater or nonexistent
      save = self.data[currIndex]
      if currIndex * 2 + 1 < len(self.data):
        if self.comp(self.data[currIndex * 2], self.data[currIndex * 2 + 1]) == 1:
          if self.comp(self.data[currIndex * 2 + 1], save) == 1: break
          self.data[currIndex] = self.data[currIndex * 2 + 1]
          self.data[currIndex * 2 + 1] = save
          currIndex = currIndex * 2 + 1
        else:
          if self.comp(self.data[currIndex * 2], save) == 1: break
          self.data[currIndex] = self.data[currIndex * 2]
          self.data[currIndex * 2] = save
          currIndex = currIndex * 2
      elif currIndex * 2 < len(self.data):
        if self.comp(self.data[currIndex * 2], save) == 1: break
        else:
          self.data[currIndex] = self.data[currIndex * 2]
          self.data[currIndex * 2] = save
          break
      else:
        break
    return output

  def peek(self):
    if len(self.data) == 1: return None
    return self.data[1]

  def toList(self):
    lst = []
    for i in range(len(self.data) - 1):
      lst.append(self.pop())
    return lst


# In[ ]:


class Node():

    def __init__(self,inval,indist,innodelst,indistA = None):
        self.val = inval
        self.dist = indist
        self.nodelst = innodelst
        self.distAStar = indistA

    def nodeComparator(a,b):
        if a.dist > b.dist: return 1
        if a.dist == b.dist: return 0
        return -1

def doubletsUninformed(a,b):
    nodeQueue = Pqueue(comparator = Node.nodeComparator)
    if len(a) != len(b): return [a,b]
    if not(len(a) in words.keys()): return [a,b]
    if not(a in words[len(a)]): return [a,b]
    if not(len(a) in neighbors.keys()):
        neighborsN(len(a), words, neighbors)
    currDict = neighbors[len(a)]
    exploredSet = set()
    currNode = Node(a,0,[])
    nodeQueue.push(currNode)
    while not(b in exploredSet):
        currNode = nodeQueue.pop()
        if currNode == None:
            return [a,b]
        lst = []
        for i in currNode.nodelst:
            lst.append(i)
        lst.append(currNode.val)
        for i in currDict[currNode.val]:
            if i in exploredSet:
                continue
            newNode = Node(i,currNode.dist + 1,lst)
            nodeQueue.push(newNode)
        exploredSet.add(currNode.val)
    currNode.nodelst.append(b)
    return currNode.nodelst

def dist(a,b):
    out = 0
    for i in range(len(a)):
        if a[i] != b[i]: out += 1
    return out

def doubletsGreedy(a,b):
    nodeQueue = Pqueue(comparator = Node.nodeComparator)
    if len(a) != len(b): return [a,b]
    if not(len(a) in words.keys()): return [a,b]
    if not(a in words[len(a)]): return [a,b]
    if not(len(a) in neighbors.keys()):
        neighborsN(len(a), words, neighbors)
    currDict = neighbors[len(a)]
    exploredSet = set()
    currNode = Node(a,dist(a,b),[])
    nodeQueue.push(currNode)
    while not(b in exploredSet):
        currNode = nodeQueue.pop()
        if currNode == None:
            return [a,b]
        lst = []
        for i in currNode.nodelst:
            lst.append(i)
        lst.append(currNode.val)
        for i in currDict[currNode.val]:
            if i in exploredSet:
                continue
            newNode = Node(i,dist(i,b),lst)
            nodeQueue.push(newNode)
        exploredSet.add(currNode.val)
    currNode.nodelst.append(b)
    return currNode.nodelst


def doubletsAStar(a,b):
    nodeQueue = Pqueue(comparator = Node.nodeComparator)
    if len(a) != len(b): return [a,b]
    if not(len(a) in words.keys()): return [a,b]
    if not(a in words[len(a)]): return [a,b]
    if not(len(a) in neighbors.keys()):
        neighborsN(len(a), words, neighbors)
    currDict = neighbors[len(a)]
    exploredSet = set()
    currNode = Node(a,dist(a,b),[],0)
    nodeQueue.push(currNode)
    while not(b in exploredSet):
        currNode = nodeQueue.pop()
        if currNode == None:
            return [a,b]
        lst = []
        for i in currNode.nodelst:
            lst.append(i)
        lst.append(currNode.val)
        for i in currDict[currNode.val]:
            if i in exploredSet:
                continue
            newNode = Node(i,dist(i,b) + (currNode.distAStar + 1),lst,currNode.distAStar + 1)
            nodeQueue.push(newNode)
        exploredSet.add(currNode.val)
    currNode.nodelst.append(b)
    return currNode.nodelst

def findlongest(n):
    longest = []
    for i in range(len(words[n])):
        for j in range(i+1,len(words[n])):
            curr = doubletsAStar(words[n][i],words[n][j])
            if len(curr) > len(longest): longest = curr
    return longest

def writeOut(infile,outfile):
    infile = open(infile,'r').read().split('\n')
    outfile = open(outfile,'w')
    wordslst = []
    for i in infile:
        curr = i.split(',')
        if len(curr) != 2: continue
        wordslst.append(curr)
    for i in wordslst:
        path = doubletsAStar(i[0],i[1])
        out = i[0]
        for j in path[1:]:
            out += ',' + j
        out += '\n'
        outfile.write(out)

writeOut(sys.argv[1],sys.argv[2])
