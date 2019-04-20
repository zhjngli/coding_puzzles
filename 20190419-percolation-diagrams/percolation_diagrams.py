#!/usr/bin/env python

# Lisa is studying patterns in an NxN grid. The patterns she's interested in are called percolation patterns. Such patterns are formed when white pixels are embedded in an NxN grid of black pixels in such a way that:
# each row of the grid has exactly one segment of white pixels, and
# the white segments of any two consecutive rows overlap in at least one column. 
 
# This diagram (see 'percolation_example.png') shows two of the 215401 percolation patterns that may be embedded in a 5x5 grid, as well as an invalid pattern. The bottom pattern is not a valid percolation pattern for either of two reasons:
# the white segments in rows 1 and 2 don’t share a column
# the bottom row contains more than one white segment.
 
# Lisa knows that there are far too many patterns to list, but she's still interested in counting them. She has calculated the number of valid patterns in a 50x50 grid and found that the last nine digits of the result are 665161235. 
 
# How many valid percolation patterns can be made in a 200x200 grid? (supply only the last 9 digits of this number as your answer) 

import functools

def triangular_num(n):
    return sum(range(1,n+1))

@functools.lru_cache(maxsize=20100)
def range_from_triangular_index(n, idx):
    '''
    calculate a range of indices (inclusive) from a number and an index
    e.g.:
    n = 3, `i` can be [0, 6)
        i = 0 -> [0,0]
        i = 1 -> [1,1]
        i = 2 -> [2,2]
        i = 3 -> [0,1]
        i = 4 -> [1,2]
        i = 5 -> [0,2]
    The range represents continuous segments, and the number of possible ranges is determined by the triangular number of `n`
    '''
    idx = idx % triangular_num(n)
    t = 0
    s, l = 0, 0
    number_of_segments = list(range(n, 0, -1)) # 3, 2, 1
    for i in range(len(number_of_segments)):
        t += number_of_segments[i]
        if t > idx:
            s = (idx - t + number_of_segments[i]) % n
            l = i
            break
    return s, s + l

def overlap(s1, e1, s2, e2):
    return (s2 >= s1 and s2 <= e1) or (e2 >= s1 and e2 <= e1)

@functools.lru_cache(maxsize=200)
def index_overlaps_with_triangular_index(n, idx):
    '''
    calculate a list of indices which have overlap with the segment represented by a triangular index
    '''
    l = []
    s, e = range_from_triangular_index(n, idx)
    for i in range(triangular_num(n)):
        si, ei = range_from_triangular_index(n, i)
        if overlap(s, e, si, ei):
            l.append(i)
    return l

def percolation_diagrams(r, c):
    '''
    calculate the number of percolation diagrams for r rows and c columns
    '''
    # create 2d array of r rows and triangular number of c columns, initialized to 1
    # each value in the 2d array will represent the number of valid percolation patterns at that row and ending with the segment represented by that indexed triangular number
    p = [[1 for _ in range(triangular_num(c))] for _ in range(r)]
    # start from the second row and calculate each value
    for i in range(1, len(p)):
        for j in range(len(p[i])):
            idxs = index_overlaps_with_triangular_index(c, j)
            p[i][j] = 0
            for idx in idxs:
                p[i][j] += p[i-1][idx]
    # return sum of the last row
    return sum(p[-1])

n = 50
print(percolation_diagrams(n, n))
