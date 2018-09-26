#!/usr/bin/python3
import sys

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

add(sys.argv[1],sys.argv[2])
