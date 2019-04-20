# Lisa is studying patterns in an NxN grid. The patterns she's interested in are called percolation patterns. Such patterns are formed when white pixels are embedded in an NxN grid of black pixels in such a way that:
# each row of the grid has exactly one segment of white pixels, and
# the white segments of any two consecutive rows overlap in at least one column. 
 
# This diagram (see 'percolation_example.png') shows two of the 215401 percolation patterns that may be embedded in a 5x5 grid, as well as an invalid pattern. The bottom pattern is not a valid percolation pattern for either of two reasons:
#   - the white segments in rows 1 and 2 don’t share a column
#   - the bottom row contains more than one white segment.
 
# Lisa knows that there are far too many patterns to list, but she's still interested in counting them. She has calculated the number of valid patterns in a 50x50 grid and found that the last nine digits of the result are 665161235. 
 
# How many valid percolation patterns can be made in a 200x200 grid? (supply only the last 9 digits of this number as your answer)

class PercolationDiagrams:
    def __init__(self, r, c, last_digits=9):
        self.r = r
        self.c = c
        self.last_digits = last_digits
        self.t = self._triangular_num(c)
        self._calculate_ranges()
        self._calculate_overlaps()
        print("done initializing!")

    def _triangular_num(self, n):
        return sum(range(1,n+1))

    def _overlap(self, s1, e1, s2, e2):
        return (s2 >= s1 and s2 <= e1) or (e2 >= s1 and e2 <= e1) or \
               (s1 >= s2 and s1 <= e2) or (e1 >= s2 and e1 <= e2)

    def _calculate_ranges(self):
        '''
        for all indices within the triangular number:
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
        self.ranges = {}
        for idx in range(self.t):
            t = 0
            s, l = 0, 0
            number_of_segments = list(range(n, 0, -1)) # 3, 2, 1
            for i in range(len(number_of_segments)):
                t += number_of_segments[i]
                if t > idx:
                    s = (idx - t + number_of_segments[i]) % n
                    l = i
                    break
            self.ranges[idx] = (s, s+l)

    def _calculate_overlaps(self):
        '''
        for all indices within the triangular number:
        calculate a list of indices which have overlap with the segment represented by a triangular index
        '''
        self.overlaps = {}
        for idx in range(self.t):
            l = []
            s, e = self.ranges[idx]
            for i in range(self.t):
                si, ei = self.ranges[i]
                if self._overlap(s, e, si, ei):
                    l.append(i)
            
            self.overlaps[idx] = l

    def calculate(self):
        # create 2d array of r rows and triangular number of c columns, initialized to 1
        # each value in the 2d array will represent the number of valid percolation patterns at that row and ending with the segment represented by that indexed triangular number
        p = [[1 for _ in range(self.t)] for _ in range(self.r)]

        # start from the second row and calculate each value
        for i in range(1, len(p)):
            print("calculating row: ", i+1)
            for j in range(len(p[i])):
                idxs = self.overlaps[j]
                p[i][j] = 0
                for idx in idxs:
                    p[i][j] += p[i-1][idx]
                
                if self.last_digits:
                    p[i][j] %= 10**self.last_digits
        
        # return sum of the last row
        s = sum(p[-1])
        if self.last_digits:
            s %= 10**self.last_digits
        return s


if __name__ == "__main__":
    import time

    n = 200

    t1 = time.process_time()
    a = PercolationDiagrams(n, n, last_digits=9)
    print(a.calculate())
    t2 = time.process_time()

    print("it took: ", t2-t1, "seconds")
