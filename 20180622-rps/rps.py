# https://fivethirtyeight.com/features/the-riddlers-inaugural-rock-paper-scissors-tournament/
# rock     0
# paper    1
# scissors 2

import numpy as np
from sympy.utilities.iterables import multiset_permutations
from collections import defaultdict
from random import shuffle

# maps a throw to the losing throw
winmap = {0: 2, 1: 0, 2: 1}


def get_throw(p):
    return np.random.choice(a=list(winmap.keys()), p=p)


def fight(p1, p2):
    # p is a (4, 3) array
    # p[3] are the initial probabilities
    # p[0-2] are the conditional proabilities given rock/paper/scissors
    p1c = 0
    p2c = 0
    i = 0
    # get initial probabilities
    p1t = get_throw(p1[3])
    p2t = get_throw(p2[3])
    while p1c < 2 and p2c < 2:  # best 2 out of 3
        if winmap[p1t] == p2t:  # p1 beats p2
            p1c += 1
        elif winmap[p2t] == p1t:  # p2 beats p1
            p2c += 1

        # get throws based on what the other threw
        p1t = get_throw(p1[p2t])
        p2t = get_throw(p2[p1t])

        i += 1
        if i > 100:  # probably a draw
            break
    
    if p1c == 2:
        return p1
    elif p2c == 2:
        return p2
    else:
        return 'draw'


def fight_strats(strats):
    shuffle(strats)
    print('pitting', len(strats), 'strategies against each other.')

    total_fights = 0
    strat_wins = defaultdict(int)
    for i1, s1 in enumerate(strats):
        for i2, s2 in enumerate(strats):
            result = fight(s1, s2)
            total_fights += 1
            if np.array_equal(result, s1):
                strat_wins[i1] += 1
            elif np.array_equal(result, s2):
                strat_wins[i2] += 1
            elif result == 'draw':
                # print('draw occurred!')
                # print(s1)
                # print(s2)
                # print('\n\n')
                continue
            else:
                print('arrays not equal????')
                print(i1, s1)
                print(i2, s2)
                print(result)

    print('There were', total_fights, 'total fights.\n')

    print(strats[max(strat_wins, key=strat_wins.get)], 'won with', max(strat_wins.values()), 'wins.\n')
    num_winners_to_print = 5
    printed_winners = 0
    print('\nThe top', num_winners_to_print, 'winners are:\n')
    for strat_index, wins in sorted(strat_wins.items(), key=lambda kv: (kv[1], kv[0]), reverse=True):
        print(strats[strat_index], 'has', wins, 'wins.\n')
        printed_winners += 1
        if printed_winners > num_winners_to_print:
            break

    num_losers_to_print = 5
    printed_losers = 0
    print('\nThe top', num_losers_to_print, 'losers are:\n')
    for strat_index, wins in sorted(strat_wins.items(), key=lambda kv: (kv[1], kv[0])):
        print(strats[strat_index], 'has', wins, 'wins.\n')
        printed_losers += 1
        if printed_losers > num_losers_to_print:
            break


if __name__ == "__main__":
    def get_random_strat():
        p = np.random.random((4, 3))
        for i in range(len(p)):
            p[i] /= p.sum(1)[i]
        return p


    def get_all_in_strats():
        strats = []
        allin = np.array([1, 0, 0])
        for r in multiset_permutations(allin):
            for p in multiset_permutations(allin):
                for s in multiset_permutations(allin):
                    for i in multiset_permutations(allin):
                        strats.append(np.array([r, p, s, i]))
        return strats


    def get_beat_strats_with_random_initial(n):
        strats = []
        for i in range(n):
            p = np.random.random(3)
            p /= p.sum()
            s = np.asarray([[0, 1, 0], [0, 0, 1], [1, 0, 0], p])
            strats.append(s)
        return strats
    

    # full neutral strategy
    neutral_strat = np.full((4, 3), 1.0/3)
    # random strategies
    num_random_strats = 100
    random_strats = [get_random_strat() for i in range(num_random_strats)]
    # all_in strategies
    all_in_strats = get_all_in_strats()
    # play whatever beats what the opponent just played
    beat1 = np.asarray([[0, 1, 0], [0, 0, 1], [1, 0, 0], [1, 0, 0]])
    beat2 = np.asarray([[0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 1, 0]])
    beat3 = np.asarray([[0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 0, 1]])
    beat4 = np.asarray([[0, 1, 0], [0, 0, 1], [1, 0, 0], [1.0/3, 1.0/3, 1.0/3]])
    # play whatever beats what the opponent just played, with random initial probabilities
    num_beat_strats = 100
    beat_strats = get_beat_strats_with_random_initial(num_beat_strats)

    # choose which strategies to use in this round
    strats = []
    strats.append(neutral_strat)
    strats.extend(random_strats)
    strats.extend(all_in_strats)
    # strats.append(beat1)
    # strats.append(beat2)
    # strats.append(beat3)
    strats.append(beat4)
    strats.extend(beat_strats)

    fight_strats(strats)
