#! /usr/bin/python3

## Mike Jovanovich
## 9/6/2015

## Reads a pair of strings from a filename specified on the cmd-line.
## Each string is a single line by itself.
## Whitespace and comment lines are skipped.
## 
## The program will align the pair of strings according to the 
## Needleman-Wunsch algorithm.
##
## When there are choices in the traceback step, diagonal is cosen, 
## then left, and finally up
##
## There a special case in which you may get to the leftmost column before 
## top row - keep the remaining chars from the top string matched
## with '-'; similarly for getting to top row before left column.
## 
## Alignment prints to stdout with the first string in the input printed
## first on the output.
##
## Sample input:
##     # this is a comment (a # in column 1 designates a comment)
##     ACGT
##     ACT
## 
## Sample output for the above input:
##     ACGT
##     AC-T
##
## Arguments:
##     ./needleman-wunsch filename  match_value  mismatch_penalty  gap_penalty
## Example run:
##     ./needleman-wunsch input.txt +5  -4  -8
## 

import sys

def main():
    if len(sys.argv) != 5:
        print("This program requires five arguments.")
        return

    # Get command line args
    filename = sys.argv[1]
    match_value = int(sys.argv[2])
    mismatch_penalty = int(sys.argv[3])
    gap_penalty = int(sys.argv[4])

    # Get strings from file
    s1 = "" 
    s2 = ""
    with open(filename,'r') as f:
        for line in f:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            if s1 == "":
                s1 = line
            else:
                s2 = line

    c1 = len(s1)+1
    c2 = len(s2)+1
    vals = [[0]*c1 for i in range(c2)]
    dirs = [['x']*c1 for i in range(c2)]

    # Calculate Needleman / Wunsch values
    for i in range(1,c2):
        for j in range(1,c1):
            match = s1[j-1] == s2[i-1]
            d = vals[i-1][j-1] + (match_value if match else mismatch_penalty)
            l = vals[i][j-1] + gap_penalty
            t = vals[i-1][j] + gap_penalty
            vals[i][j] = max(d,l,t)

            if vals[i][j] == d:
                dirs[i][j] = 'd'
            elif vals[i][j] == l:
                dirs[i][j] = 'l'
            else:
                dirs[i][j] = 't'

    # Traceback
    row = c2-1
    col = c1-1
    result1 = ""
    result2 = ""

    maxlen = max(len(s1),len(s2))
    while (row > 0 or col > 0): 
        if col == 0:
            result1 += '-'
            result2 += s2[row-1]
            row-=1
        elif row== 0:
            result1 += s1[col-1]
            result2 += '-'
            col-=1
        elif dirs[row][col] == 'd':
            result1 += s1[col-1]
            result2 += s2[row-1]
            row-=1
            col-=1
        elif dirs[row][col] == 'l':
            result1 += s1[col-1]
            result2 += '-'
            col-=1
        elif dirs[row][col] == 't':
            result1 += '-'
            result2 += s2[row-1]
            row-=1

    sys.stdout.write(result1[::-1] + "\r\n")
    sys.stdout.write(result2[::-1] + "\r\n")

main()
