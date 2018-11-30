#! /usr/bin/python3

import copy
import sys
import time

universal = set()
for i in range(1,10):
    universal.add(str(i))
numBacktracks = 0

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

def solveBoard(board):
    start = time.time()
    currBoard = board
    for i in range(9):
        currBoard[i] = currBoard[i].split(',')
    solveBoardHelper(board)
    print(time.time() - start,numBacktracks)
    return board

def solveBoardHelper(board):
    global numBacktracks
    inverse = forceBoard(board,genNeighbors(board))
    currNeighbors = genNeighbors(board)
    nextGuess = getLeast(board,currNeighbors)
    if nextGuess == None:
        if isSolved(currNeighbors):
            return True
        numBacktracks += 1
        revertBoard(inverse,board)
        return False
    guesses = universal - currNeighbors[(nextGuess[1:])]
    for i in guesses:
        board[nextGuess[1]][nextGuess[2]] = i
        if solveBoardHelper(board):
            return True
    board[nextGuess[1]][nextGuess[2]] = "_"
    numBacktracks += 1
    revertBoard(inverse,board)
    return False

def revertBoard(inverse,board):
    for i in inverse:
        board[i[0]][i[1]] = "_"

def isSolved(neighbors):
    for i in neighbors.keys():
        if len(neighbors[i]) < 9: return False
    return True

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

def printBoard(board):
    sub = ""
    for i in board:
        for j in i:
            sub += j + " "
        sub += '\n'
    print(sub + '\n')

def forceBoard(board,neighbors):
    inverse = set()
    change = True
    while change:
        change = False
        for i in range(9):
            for j in range(9):
                if board[i][j] == "_" and len(neighbors[(i,j)]) == 8:
                    for k in (universal - neighbors[(i,j)]):
                        updateNeighbors(neighbors,(i,j,k))
                        board[i][j] = k
                        inverse.add((i,j))
                        change = True
    return inverse

def getLeast(board,neighbors):
    least = None
    for i in range(9):
        for j in range(9):
            curr = len(neighbors[(i,j)])
            if board[i][j] == "_" and curr != 9:
                if curr == 7: return (curr,i,j)
                if least == None:
                    least = (curr,i,j)
                elif curr > least[0]:
                    least = (curr,i,j)
    return least

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
