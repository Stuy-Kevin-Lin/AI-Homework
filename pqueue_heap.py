#! /usr/bin/python3
'''
Algorithms:
Note: Node.swap(other) swaps the values of the two Nodes rather than the actual
      Nodes because that's less work for both me and the computer.
    pop(): Saves the root value, swaps the values of the root and last Node,
deletes last Node, then from the root, swaps with the lesser child until the heap
is balanced, and finally, returns the original root value
    push(val): First, ask the last Node if it is a left child. If it is, then
ask its parent to set their right child to a new Node containing the value.
If it isn't, ask the parent's parent to check for all possible openings of its
right child, unless the parent itself is a right child. If an opening is not
found or the parent is a right child, ask the parent's parent's parent the same
thing, except now check if the parent's parent is a left or right child. This
continues until an opening is found or the root of the heap is reached. If the
root of the heap is reached, then go down the left until an opening is found and
add the new Node there. At this point, you should have a new Node. Until the heap
is balanced, swap the new Node with its parent if the parent is greater.
    toheap(): If the heap is empty, return an empty string. Otherwise, create a
new list and ask the root to run toHeap(lst, level = 0). If level is out of
bounds for lst, then lst will be appended with a new list with a single element
equal to the Node's data. It will then ask its left and right child to run
toHeap(lst, level + 1) if they exist, and in that order. toheap() then outputs
a string using the lists inside lst as rows.

Node variables:
data - Stores the Node's information
prevNode - Pointer to the previously added Node in the heap
leftright - Stores whether the Node is a left or right child
parent - Pointer to the Node's parent
left - Pointer to the Node's left child
right - Pointer to the Node's right child
'''

import sys

class PriorityQueue(): #Tree version

    def defaultComp(a,b):
        if a.data > b.data: return 1
        if a.data == b.data: return 0
        return -1

    def __init__(self, comparator = defaultComp):
        self.root = None
        self.last = None
        self.comp = comparator

    def peek(self):
        if self.root == None: return None
        return self.root.data

    def pop(self):
        if self.root == None: return None
        output = self.root.data
        if self.root.left == None and self.root.right == None:
            self.root = None
            self.last = None
            return output

        self.root.data = self.last.data #Move last to root
        self.last = self.last.remove()

        currNode = self.root
        while True:
            if currNode.left == None: return output
            if currNode.right == None:
                if self.comp(currNode, currNode.left) == 1:
                    currNode.swap(currNode.left)
                return output
            else:
                if self.comp(currNode.left, currNode.right) == -1:
                    if self.comp(currNode, currNode.left) == 1:
                        currNode.swap(currNode.left)
                        currNode = currNode.left
                    else: return output
                else:
                    if self.comp(currNode, currNode.right) == 1:
                        currNode.swap(currNode.right)
                        currNode = currNode.right
                    else: return output

    def push(self, value):

        if self.root == None:
            self.root = Node(value, None, "N/A", None)
            self.last = self.root
            return True

        if self.root == self.last:
            self.root.left = Node(value, self.root, "left", self.root)
            self.last = self.root.left
            if self.comp(self.last, self.root) == -1: self.last.swap(self.root)
            return True

        if self.last.leftright == "left":
            self.last.parent.right = Node(value, self.last, "right", self.last.parent)
            self.last = self.last.parent.right

        elif self.last.leftright == "right":
            levelChange = -1
            save = self.last
            openNode = None
            while True: #Find empty position
                if save.parent == None:
                    openNode = self.root
                    while openNode.left != None:
                        openNode = openNode.left
                    break
                openNode = save.parent.findOpen(levelChange, save.leftright)
                if openNode == None:
                    levelChange -= 1
                    save = save.parent
                    continue
                else:
                    break
            if openNode.left == None:
                openNode.left = Node(value, self.last, "left", openNode)
                self.last = openNode.left
            else:
                openNode.right = Node(value, self.last, "right", openNode)
                self.last = openNode.right

        newNode = self.last
        while newNode.parent != None and self.comp(newNode, newNode.parent) == -1:
            newNode.swap(newNode.parent)
            newNode = newNode.parent

        return True

    def tolist(self):
        lst = []
        while self.root != None:
            lst.append(self.pop())
        return lst

    def toheap(self):
        if self.root == None: return ""
        lst = []
        self.root.toHeap(lst,0)
        output = ""
        #print(lst)
        for i in lst:
            subs = "out: "
            for j in i:
                subs += j + ","
            output += subs[:-1] + "\n"
        output = output[:-1]
        #print(output + "\n-----------")
        return output

class Node():

    def __init__(self, value, inputLast, left, par):
        self.data = value
        self.prevNode = inputLast
        self.leftright = left
        self.parent = par
        self.left = None
        self.right = None

    def swap(self,other):
        save = other.data
        other.data = self.data
        self.data = save

    def remove(self):
        if (self.leftright == "left"): self.parent.left = None
        else: self.parent.right = None
        return self.prevNode

    def findOpen(self, levelChange, origin = None):
        if origin == "right": return None
        if levelChange == 0: return None
        elif self.left == None or self.right == None: return self
        return self.right.findOpen(levelChange + 1)

    def toHeap(self, lst, level):
        if level > len(lst) - 1:
            lst.append([self.data])
        else:
            lst[level].append(self.data)
        if self.left != None:
            self.left.toHeap(lst, level + 1)
        if self.right != None:
            self.right.toHeap(lst, level + 1)

def strComp(a,b):
    index = 0
    if a.data == b.data: return 0
    while True:
        if index >= len(a.data): return 1
        if index >= len(b.data): return -1
        if ord(a.data[index]) > ord(b.data[index]): return 1
        if ord(a.data[index]) < ord(b.data[index]): return -1
        if ord(a.data[index]) == ord(b.data[index]):
            index += 1

def test(inFile, outFile):
    newPQ = PriorityQueue(comparator = strComp)
    inFile = open(inFile,"r").read()
    inFile = inFile.split("\n")
    inFile = inFile[:-1]
    commands = []
    for i in inFile:
        commands.append(i)
    outFile = open(outFile,"w")
    for i in range(len(inFile)):
        inFile[i] = inFile[i].split(",")
    #print(inFile)
    index = 0
    for i in inFile:
        outFile.write("in: " + commands[index] + "\n")
        index += 1
        if i[0] == "push":
            for elm in i[1:]:
                newPQ.push(elm)
        elif i[0] == "peek":
            outFile.write("out: " + str(newPQ.peek()) + "\n")
        elif i[0] == "pop":
            outFile.write("out: " + str(newPQ.pop()) + "\n")
        elif i[0] == "tolist":
            output = "out: "
            lst = newPQ.tolist()
            if len(lst) == 0: pass
            else:
                for i in lst:
                    output += i + ","
                output = output[:-1]
            outFile.write(output + "\n")
        elif i[0] == "toheap":
            outFile.write(newPQ.toheap() + "\n")

test(sys.argv[1],sys.argv[2])
