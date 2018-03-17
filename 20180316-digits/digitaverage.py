#!/usr/bin/env python

def avgofdigits(digitlist):
    avg = 0.0
    for digit in digitlist:
        avg += digit
    return avg/len(digitlist)

def valofdigits(digitlist):
    val = 0
    for i in range(len(digitlist)):
        val += digitlist[i] * 10**(-i)
    return val

def inttodigitlist(i):
    digitlist = []
    while i != 0:
        digitlist.insert(0, i % 10)
        i /= 10
    return digitlist

def main():
    for md in range(1, 8):
        MAX_DIGITS = md
        print 'looking for numbers in range (', 10**(MAX_DIGITS-1), ',', 10**MAX_DIGITS, ')'
        formatstr = '.' + str(MAX_DIGITS-1) + 'f'
        for i in range(10**(MAX_DIGITS-1), 10**MAX_DIGITS):
            if i % 10 == 0:
                continue
            digitlist = inttodigitlist(i)
            avg = format(avgofdigits(digitlist), formatstr)
            val = format(valofdigits(digitlist), formatstr)
            if avg == val:
                print digitlist

if __name__ == "__main__":
    main()
