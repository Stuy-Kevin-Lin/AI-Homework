#! /usr/bin/python3

import copy
import sys

class Stack:

    def __init__(self):
        self.inside = []

    def push(self,val):
        self.inside.append(val)

    def pop(self):
        if len(self.inside) == 0: return None
        return self.inside.pop()

    def peek(self):
        if len(self.inside) == 0: return None
        return self.inside[-1]

def genCliques(input):
    rows = []
    cols = []
    boxes = []
    for i in range(9):
        cols.append([])
        boxes.append([])
    for i in range(9):
        curr = input[i]
        rows.append(curr)
        for j in range(9):
            cols[j].append(curr[j])
        boxesPos = i//3 * 3
        ctr = 0
        for j in range(boxesPos,boxesPos+3):
            for k in range(3):
                boxes[j].append(curr[ctr])
                ctr += 1
    return [rows,cols,boxes]

def genNeighbors(board):
    cliques = genCliques(board)
    output = dict()
    for i in range(9):
        for j in range(9):
            pos = (i,j)
            output[pos] = neighborsSet(cliques,pos)
    return output

def neighborsSet(cliques,cellPos):
    #cellPos = (row,col)
    output = set()
    for i in cliques[0][cellPos[0]]:
        if (i != "_"):
            output.add(i)
    for i in cliques[1][cellPos[1]]:
        if (i != "_"):
            output.add(i)
    boxPos = (cellPos[1]//3) + (cellPos[0]//3 * 3)
    for i in cliques[2][boxPos]:
        if (i != "_"):
            output.add(i)
    return output

def updateNeighbors(neighbors,update):
    inverse = set()
    boxPos = (update[0]//3 * 3,update[1]//3 * 3)
    for i in range(9):
        if not(str(update[2]) in neighbors[(update[0],i)]):
            neighbors[(update[0],i)].add(str(update[2]))
            inverse.add((update[0],i,str(update[2])))
        if not(str(update[2]) in neighbors[(i,update[1])]):
            neighbors[(i,update[1])].add(str(update[2]))
            inverse.add((i,update[1],str(update[2])))
    for i in range(boxPos[0],boxPos[0]+3):
        for j in range(boxPos[1],boxPos[1]+3):
            if not(str(update[2]) in neighbors[(i,j)]):
                neighbors[(i,j)].add(str(update[2]))
                inverse.add((i,j,str(update[2])))
    return inverse

def revertNeighbors(neighbors,inverse):
    for i in inverse:
        if i[2] in neighbors[(i[0],i[1])]:
            neighbors[(i[0],i[1])].remove(i[2])

def solveBoard(board):
    guessStack = Stack()
    neighborsStack = Stack()
    row = 0
    col = 0
    prevNum = 0
    currBoard = board
    for i in range(9):
        currBoard[i] = currBoard[i].split(',')
    currNeighbors = genNeighbors(currBoard)
    backtrackCtr = 0
    ctr = 1
    while row < 9:
        while col < 9:
            if currBoard[row][col] == "_":
                for i in range(prevNum+1,10):
                    if not(str(i) in currNeighbors[(row,col)]):
                        ctr += 1
                        prevNum = 0
                        currGuess = (row,col,i,currBoard[row][col])
                        neighborsStack.push(updateNeighbors(currNeighbors,currGuess))
                        guessStack.push(currGuess)
                        currBoard[row][col] = str(i)
                        break
                else:
                    if guessStack.peek() == None:
                        print(backtrackCtr,ctr)
                        return currBoard
                    backtrackCtr += 1
                    revertNeighbors(currNeighbors,neighborsStack.pop())
                    row,col,prevNum,currBoard[row][col] = guessStack.pop()
                    continue
            if (col == 8) and (row == 8):
                if isSolved(currNeighbors) or guessStack.peek() == None:
                    print(backtrackCtr,ctr)
                    return currBoard
                backtrackCtr += 1
                revertNeighbors(currNeighbors,neighborsStack.pop())
                row,col,prevNum,currBoard[row][col] = guessStack.pop()
            col += 1
        row += 1
        col = 0

def isSolved(neighbors):
    for i in neighbors.keys():
        if len(neighbors[i]) < 9: return False
    return True

def printBoard(board):
    sub = ""
    for i in board:
        for j in i:
            sub += j + " "
        sub += '\n'
    print(sub + '\n')

def findIndex(lst,match):
    for i in range(len(lst)):
        if lst[i] == match: return i
    return -1

def writeSolution(boards,outfile,select):
    boards = open(boards,'r').read()
    outfile = open(outfile,'w')
    boards = boards.split('\n')
    index = findIndex(boards,select)
    if index == -1: return
    solution = solveBoard(boards[index+1:index+10])
    select = select.split(",")
    select[2] = 'solved'
    select = ','.join(select)
    outfile.write(select + '\n')
    for i in solution:
        outfile.write(i[0])
        for j in i[1:]:
            outfile.write("," + j)
        outfile.write('\n')

writeSolution(sys.argv[1],sys.argv[2],sys.argv[3])
