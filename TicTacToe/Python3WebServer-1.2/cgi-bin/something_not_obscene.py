#! /usr/bin/python

# -*- coding: utf-8 -*-
"""TicTacToe-HW3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1NxL_b3P0pU5ZmS2iWSpRGLhXLRCEDHRs

### TicTac Toe Homework 3###

We're closing in on a real competitor, with new properties of the BoardNode that will guide us to true bliss and the best next move.

Again, I'm using layout and board sometimes synonymously.
"""

#@title
import random, sys

''' Layout positions:
0 1 2
3 4 5
6 7 8
'''
# Best future states according to the player viewing this board
ST_X = 1  # X wins
ST_O = 2  # O wins
ST_D = 3  # Draw

Wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]

AllBoards = {}   # This is primarily for debugging: key = layout, value = BoardNode

class BoardNode:

    def __init__(self, layout):
        self.layout = layout
        self.mover = 'x' if layout.count('x') == layout.count('o') else 'o'

        self.state = BoardNode.this_state(layout) # if final board, then ST_X, ST_O or ST_D, else None
        if self.state is None:
            self.best_final_state = None           # best achievable future state: ST_X, ST_O or ST_D
            self.best_move = None                  # 0-9 to achieve best state
            self.num_moves_to_final_state = None   # number of moves to best state
        else:
            self.best_final_state = self.state
            self.best_move = -1
            self.num_moves_to_final_state = 0

        self.children = set()

    def print_me(self):
        print('layout:',self.layout)
        print('mover:',self.mover)
        print('state:',BoardNode.str_state(self.state))
        print('best_final_state:',BoardNode.str_state(self.best_final_state))
        print('best_move:',self.best_move,BoardNode.str_move(self.best_move))
        print('num_moves_to_final_state:',self.num_moves_to_final_state)

    def print_layout(self):
        print('%s\n%s\n%s' % (' '.join(self.layout[0:3]),' '.join(self.layout[3:6]),' '.join(self.layout[6:9])))

    # =================== class methods  =======================
    def str_state(state):
        # human description of a state
        return 'None' if state is None else ['x-wins','o-wins','draw'][state-1]

    def str_move(move):
        # human description of a move
        moves = ('top-left','top-center','top-right',\
                 'middle-left','middle-center','middle-right',\
                 'bottom-left','bottom-center','bottom-right')
        return 'done' if move == -1 else moves[move]

    def this_state(layout):
        # classifies this layout as None if not final, otherwise ST_X or ST_O or ST_D
        for awin in Wins:
            if layout[awin[0]] != '_' and layout[awin[0]] == layout[awin[1]] == layout[awin[2]]:
                return ST_X if layout[awin[0]] == 'x' else ST_O
        if layout.count('_') == 0:
            return ST_D
        return None

def CreateAllBoards(layout):
    # Populate AllBoards with finally calculated BoardNodes

    if layout in AllBoards:
        return (AllBoards[layout].best_final_state,AllBoards[layout].num_moves_to_final_state,)

    anode = BoardNode(layout)
    # if this is an end board, then all of its properties have already be calculated by __init__()
    if anode.state is not None:
        AllBoards[layout] = anode
        return (anode.state, 0)

    # expand children if this is not a final state
    move = 'x' if layout.count('x') == layout.count('o') else 'o'
    ST_W = ST_O if move == 'o' else ST_X
    ST_L = ST_O if move == 'x' else ST_X

    paths = []

    for pos in range(9):
        if layout[pos] == '_':
            new_layout = layout[:pos] + move + layout[pos+1:]
            curr = None
            if new_layout not in AllBoards:
              curr = CreateAllBoards(new_layout)
            else:
              curr = (AllBoards[new_layout].best_final_state,AllBoards[new_layout].num_moves_to_final_state)
            curr = (curr[0],curr[1] + 1,pos)
            paths.append(curr)
            anode.children.add(new_layout)

    # ==============================================================================
    # Your excellent code here to calculate the BoardNode properties below for this node
    #   best_move
    #   best_final_state
    #   num_moves_to_final_state
    # ===============================================================================

    #If winning path exists, choose shortest
    #If paths have equal lengths, choose randomly
    #If no winning path exists, choose longest path to draw
    #If no winning or draw, choose longest path

    AllBoards[layout] = anode
    bestChoice = None
    bestChoice = bestPath(paths,ST_W)
    #print(layout,paths,bestChoice)
    anode.best_final_state = bestChoice[0]
    anode.best_move = bestChoice[2]
    anode.num_moves_to_final_state = bestChoice[1]


    return (bestChoice[0],bestChoice[1])

def bestPath(pathLst,winner):
  wins = []
  loses = []
  draws = []
  for i in pathLst:
    if i[0] == winner:
      if len(wins) == 0:
        wins.append(i)
      elif wins[0][1] > i[1]:
        wins.clear()
        wins.append(i)
      elif wins[0][1] == i[1]:
        wins.append(i)
    elif i[0] == ST_D:
      if len(draws) == 0:
        draws.append(i)
      elif draws[0][1] < i[1]:
        draws.clear()
        draws.append(i)
      elif draws[0][1] == i[1]:
        draws.append(i)
    else:
      if len(loses) == 0:
        loses.append(i)
      elif loses[0][1] < i[1]:
        loses.clear()
        loses.append(i)
      elif loses[0][1] == i[1]:
        loses.append(i)
  if len(wins) != 0:
    return random.choice(wins)
  elif len(draws) != 0:
    return random.choice(draws)
  else:
    return random.choice(loses)


AllBoards = {}
inputDict = {}

for i in sys.argv[1:]:
    curr = i.split("=")
    inputDict[curr[0]] = curr[1]

output = inputDict["result_prefix"] + "\n"

if "id" in inputDict and inputDict["id"] == "1":
    output += "author=Kevin Lin\ntitle=Something not Obscene"
else:
    CreateAllBoards(inputDict["board"])
    node = AllBoards[inputDict["board"]]
    output += "move=" + str(node.best_move) + "\n" + "Best move: " + BoardNode.str_move(node.best_move) + ". "
    state = BoardNode.str_state(node.best_final_state)
    if state != None:
        state = state[0].upper() + state[1:]
        output += state + " in " + str(node.num_moves_to_final_state)
        if node.num_moves_to_final_state != 1:
            output += " moves."
        else:
            output += " move."

if "result_file" in inputDict:
    open(inputDict["result_file"],'w').write(output)
else:
    print(output)