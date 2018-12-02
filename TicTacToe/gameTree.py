#! /usr/bin/python3

''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# layouts look like "_x_ox__o_"

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {} # this is a dictionary with key = a layout, and value = its corresponding BoardNode

class BoardNode:
    def __init__(self,layout):
        self.layout = layout
        self.endState = self.checkWin(layout) # if this is a terminal board, endState == 'x' or 'o' for wins, of 'd' for draw, else None
        self.parents = self.getParents(layout) # all layouts that can lead to this one, by one move
        self.children = self.getChildren(layout,self.endState) # all layouts that can be reached with a single move

    def checkWin(self,layout):
        for i in Wins:
            startChar = layout[i[0]]
            if startChar == "_": continue
            for j in i[1:]:
                if layout[j] != startChar: break
            else:
                return startChar
        if not "_" in layout: return "d"
        return None

    def getParents(self,layout):
        if layout == "_________": return []
        output = []
        cntX = 0
        cntO = 0
        #Determines who went last
        for i in layout:
            if i == "x":
                cntX += 1
            elif i == "o":
                cntO += 1
        turn = "x"
        if cntX < cntO:
            turn = "o"
        for i in range(9):
            if layout[i] != turn: continue
            newBoard = layout[0:i] + "_" + layout[i+1:] #Removes turn
            output.append(newBoard)
        return output

    def getChildren(self,layout,endState):
        if endState != None: return []
        output = []
        cntX = 0
        cntO = 0
        #Determines who goes next
        for i in layout:
            if i == "x":
                cntX += 1
            elif i == "o":
                cntO += 1
        turn = "x"
        if cntX > cntO:
            turn = "o"
        for i in range(9):
            if layout[i] != "_": continue
            newBoard = layout[0:i] + turn + layout[i+1:] #Replaces _
            output.append(newBoard)
        return output

    def print_me(self):
        print ('layout:',self.layout, 'endState:',self.endState)
        print ('parents:',self.parents)
        print ('children:',self.children)

def CreateAllBoards(layout,parent):
    # recursive function to manufacture all BoardNode nodes and place them into the AllBoards dictionary
    global AllBoards
    if layout in AllBoards: return
    newNode = BoardNode(layout)
    AllBoards[layout] = newNode
    for i in newNode.children:
        CreateAllBoards(i,layout)

def countChildren():
    global AllBoards
    subt = 0
    for i in AllBoards.keys():
        subt += len(AllBoards[i].children)
    return subt

def boardStateCount():
    global AllBoards
    o = 0
    d = 0
    x = 0
    on = 0
    for i in AllBoards:
        curr = AllBoards[i].endState
        if curr == None: on += 1
        elif curr == "x": x += 1
        elif curr == "o": o += 1
        else: d += 1
    print("Number of x wins: " + str(x))
    print("Number of o wins: " + str(o))
    print("Number of draws: " + str(d))
    print("Number of ongoing boards: " + str(on))

CreateAllBoards("_________",None)
print("Number of boards: " + str(len(AllBoards)))
print("Number of children: " + str(countChildren()))
boardStateCount()
