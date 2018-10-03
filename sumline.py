#!/usr/bin/python3
import sys

def readPy(outfile):
    reading = open("program_tester.py","r")
    reading = reading.read().replace("\n","\\n")
    writing = open(outfile, "w")
    writing.write(reading)

def modifyIn(infile, outfile):
    infile = open(infile, "w")
    infile.write("a,b,c,d\n")
    infile.write("1,2,3,4\n")
    outfile = open(outfile, "w")
    outfile.write("10")

def add(infile, outfile):
    infile = open(infile,'r')
    infile = infile.read().split("\n")

    outfile = open(outfile,'w')
    for i in infile:
        currLine = i.split(",")
        subt = 0
        for elm in currLine:
            try:
                if eval(elm) > 0: subt+= eval(elm)
            except:
                continue
        if subt != 0: outfile.write(str(subt) + "\n")

#readPy(sys.argv[2])
#modifyIn(sys.argv[1], sys.argv[2])
#add(sys.argv[1],sys.argv[2])

reading = open("program_tester.py","w")
reading.write("Test")
#outfile = open(sys.argv[2], "w")
#outfile.write("1")
infile = sys.argv[1]
outfile = sys.argv[2]
infile = open(infile,'r')
infile = infile.read().split("\n")

outfile = open(outfile,'w')
for i in infile:
    currLine = i.split(",")
    subt = 0
    for elm in currLine:
        outfile.write("" + "\n")
        try:
            if eval(elm) > 0: subt+= eval(elm)
        except:
            continue
    if subt != 0: outfile.write(str(subt) + "\n")
