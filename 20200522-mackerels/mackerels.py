### https://fivethirtyeight.com/features/somethings-fishy-in-the-state-of-the-riddler/
### word list: https://norvig.com/ngrams/word.list

from collections import defaultdict


states_and_territories = {'alabama', 'alaska', 'americansamoa', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'districtofcolumbia', 'florida', 'georgia', 'guam', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'minoroutlyingislands', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'newhampshire', 'newjersey', 'newmexico', 'newyork', 'northcarolina', 'northdakota', 'northernmarianaislands', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'puertorico', 'rhodeisland', 'southcarolina', 'southdakota', 'tennessee', 'texas', 'usvirginislands', 'utah', 'vermont', 'virginia', 'washington', 'westvirginia', 'wisconsin', 'wyoming'}
states = {'alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware', 'districtofcolumbia', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota', 'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'newhampshire', 'newjersey', 'newmexico', 'newyork', 'northcarolina', 'northdakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania', 'rhodeisland', 'southcarolina', 'southdakota', 'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'westvirginia', 'wisconsin', 'wyoming'}


def get_word_letters_set(w):
    s = set()
    for c in w:
        s.add(c)
    return s


def get_word_to_letters_dict(ws):
    d = {}
    for w in ws:
        d[w] = get_word_letters_set(w)
    return d


def no_shared_letters(ls1, ls2):
    for l in ls1:
        if l in ls2:
            return False
    return True


def is_mackerel(word_letters_set, states_letters_dict):
    count = 0
    mackerel_state = ''
    for state, state_letters in states_letters_dict.items():
        if no_shared_letters(word_letters_set, state_letters):
            count += 1
            mackerel_state = state
        if count > 1:
            return False, mackerel_state
    return count == 1, mackerel_state


def main():
    states_letters_dict = get_word_to_letters_dict(states)
    states_mackerels = defaultdict(list)
    mackerels = []
    
    with open('word.list.txt', 'r') as words:
        for w in words:
            w = w.strip()
            wls = get_word_letters_set(w)
            b, mackerel_state = is_mackerel(wls, states_letters_dict)
            if b:
                mackerels.append((w, mackerel_state))
                states_mackerels[mackerel_state].append(w)

    
    mackerels.sort(key=lambda m: len(m[0]), reverse=True)
    n = 10
    print(f'the longest {n} mackerels are:')
    for i in range(n):
        print(f'{mackerels[i][0]}, belonging to {mackerels[i][1]}')

    num_mackerels_to_print = 5
    print(f'\nstates in order of most mackerels:')
    for state, state_mackerels in sorted(states_mackerels.items(), key=lambda i: len(i[1]), reverse=True):
        print(f'{state} has {len(state_mackerels)} mackerels. The top {num_mackerels_to_print} are {sorted(state_mackerels, key=len, reverse=True)[0:num_mackerels_to_print]}.')


if __name__ == "__main__":
    main()
