# https://fivethirtyeight.com/features/riddler-nation-goes-to-war/
# python simpwar.py | sort -t' ' -k14,14nr | head

import random

og = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
one = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
two = list(one)
two.reverse()

NUM = 100000

def compare_onetwo(l):
    lpoints = 0
    for i in range(len(one)):
        if l[i] > one[i]:
            lpoints += 1
    if lpoints < 7:
        return -1
    lpoints = 0
    for i in range(len(two)):
        if l[i] > two[i]:
            lpoints += 1
    if lpoints < 7:
        return -1

    return 0

def fight(t, s):
    tpoints = 0
    for i in range(len(t)):
        if t[i] > s[i]:
            tpoints += 1
    if tpoints >= 7:
        return 1
    else:
        return -1

beaters = {}
while len(beaters) < NUM:
    l = list(og)
    random.shuffle(l)
    if compare_onetwo(l) == 0:
        beaters[tuple(l)] = 0

for t, v in beaters.iteritems():
    for s, u in beaters.iteritems():
        if t != s:
            r = fight(list(t), list(s))
            if r == 1:
                beaters[t] += 1
            if r == -1:
                beaters[s] += 1

for k, v in beaters.iteritems():
    print k, v