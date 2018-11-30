#! /usr/bin/python3

def genTree(board):
    allBoards = set()
    return genTreeHelper(board,0,allBoards), len(allBoards)

def genTreeHelper(board,depth,allBoards):
    allBoards.add(board)
    if checkBoard(board) != "Ongoing":
        #print(board[0:3] + "\n" + board[3:6] + "\n" + board[6:] + "\n\n")
        return 1
    cntX = 0
    cntO = 0
    #Determines who goes next
    for i in board:
        if i == "x":
            cntX += 1
        elif i == "o":
            cntO += 1
    turn = "x"
    if cntX > cntO:
        turn = "o"
    ctr = 0 #Does not count a ongoing match as a game
    for i in range(9):
        if board[i] != "_": continue
        newBoard = board[0:i] + turn + board[i+1:] #Replaces _
        ctr += genTreeHelper(newBoard,depth + 1,allBoards)
    return ctr

def checkBoard(board):
    #Horizontal check
    for i in range(3):
        start = i * 3
        startChar = board[start]
        if startChar == "_": continue
        for j in range(1,3):
            if board[start + j] != startChar: break
        else:
            return startChar + " wins"
    #Vertical check
    for i in range(3):
        startChar = board[i]
        if startChar == "_": continue
        for j in range(1,3):
            if board[i + (3 * j)] != startChar: break
        else:
            return startChar + " wins"
    #Diagonal check
    center = board[4]
    if center == "_": return "Ongoing"
    if (board[0] == center and board[8] == center) or (board[2] == center and board[6] == center):
        return center + " wins"
    #Draw check
    for i in board:
        if i == "_": break
    else: return "Draw"
    return "Ongoing"

print(genTree("_________"))
