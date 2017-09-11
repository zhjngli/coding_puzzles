# https://fivethirtyeight.com/features/riddler-nation-goes-to-war/
# based on http://www.bicyclecards.com/how-to-play/war/
from collections import deque
import random
from datetime import datetime

class OutOfCardsError(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '%s %s' % (self.name, 'out of cards during war')

class Deck():
    def __init__(self, name, cards):
        self.name = name
        self.cards = deque(cards)

    def shuffle(self):
        random.shuffle(self.cards)

    def len(self):
        return len(self.cards)

    def append(self, c):
        self.cards.append(c)

    def extend(self, cs):
        self.cards.extend(cs)

    def deal_one(self):
        try:
            c = self.cards.popleft()
        except IndexError:
            raise OutOfCardsError(self.name)
        return c

allaces = [14, 14, 14, 14]
othercards = [ 2,  2,  2,  2,
               3,  3,  3,  3,
               4,  4,  4,  4,
               5,  5,  5,  5,
               6,  6,  6,  6,
               7,  7,  7,  7,
               8,  8,  8,  8,
               9,  9,  9,  9,
              10, 10, 10, 10,
              11, 11, 11, 11,
              12, 12, 12, 12,
              13, 13, 13, 13]

def war(warpile, one, two):
    # deal face down cards
    try:
        fdo = one.deal_one()
    except OutOfCardsError:
        two.extend(warpile)
        return
    try:
        fdt = two.deal_one()
    except OutOfCardsError:
        one.append(fdo)
        one.extend(warpile)
        return
    fdc = [fdo, fdt]
    # add face down cards to war pile in random order
    random.shuffle(fdc)
    warpile.extend(fdc)
    # deal face up cards
    try:
        fuo = one.deal_one()
    except OutOfCardsError:
        two.extend(warpile)
        return
    try:
        fut = two.deal_one()
    except OutOfCardsError:
        one.append(fuo)
        one.extend(warpile)
        return
    fuc = [fuo, fut]
    random.shuffle(fuc)
    warpile.extend(fuc)
    if fuo > fut:
        # one takes the warpile
        one.extend(warpile)
    elif fut > fuo:
        # two takes the warpile
        two.extend(warpile)
    else:
        # go to war again
        war(warpile, one, two)

def simulate_game(decks):
    rounds = 0
    order = [decks[1], decks[0]]
    while decks[0].len() > 0 and decks[1].len() > 0:
        rounds += 1
        order.reverse()
        one = order[0]
        two = order[1]
        # both players turn up a card
        o = one.deal_one()
        t = two.deal_one()
        if o > t:
            # one takes both cards
            one.append(o)
            one.append(t)
        elif t > o:
            # two takes both cards
            two.append(t)
            two.append(o)
        else:
            # go to war
            warpile = [t, o]
            random.shuffle(warpile)
            try:
                war(warpile, one, two)
            except OutOfCardsError as e:
                # print e, 'in', rounds, 'rounds'
                print 'this should literally never happen'
                break
    return rounds
    if decks[0].len() == 0:
        print decks[0].name, 'lost in', rounds, 'rounds'
        print decks[1].cards, decks[1].len()
    if decks[1].len() == 0:
        print decks[1].name, 'lost in', rounds, 'rounds'
        print decks[0].cards, decks[0].len()

def main():
    NUM = 200000000
    aceswin = 0
    aceswin_avgrounds = 0
    aceslose_avgrounds = 0
    print 'running war simulation', NUM, 'times\n\n'
    start = datetime.now()
    for i in range(0, NUM):
        aces = Deck('aces', allaces)
        oths = Deck('oths', othercards)
        aces.shuffle()
        oths.shuffle()
        decks = [aces, oths]
        rounds = simulate_game(decks)
        if aces.len() == 0:
            aceslose_avgrounds += rounds
        if oths.len() == 0:
            aceswin += 1
            aceswin_avgrounds += rounds

        if i % 10000 == 0:
            curr = datetime.now()
            elapsed = float(curr.microsecond - start.microsecond)/1000
            print 'elapsed time:', elapsed, 'milliseconds'
            print 'All aces win', (float(aceswin)/(i+1)), 'times'
            print 'On average, all aces win in', (float(aceswin_avgrounds)/(i+1)), 'rounds'
            print 'On average, all aces lose in', (float(aceslose_avgrounds)/(i+1)), 'rounds'
            print '\n'

    curr = datetime.now()
    elapsed = float(curr.microsecond - start.microsecond)/1000
    print 'elapsed time:', elapsed, 'milliseconds'
    print 'All aces win', (float(aceswin)/NUM), 'times'
    print 'On average, all aces win in', (float(aceswin_avgrounds)/NUM), 'rounds'
    print 'On average, all aces lose in', (float(aceslose_avgrounds)/NUM), 'rounds'

if __name__ == "__main__":
    main()
