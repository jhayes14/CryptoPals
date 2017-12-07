"""
    https://cryptopals.com/sets/1/challenges/4
"""

from cryptofuncs import *

if __name__ == "__main__":
    L = [ ]
    with open('../inputs/4.txt') as ciphers:
        possible_keys = [x for x in range(256)]
        for ctext in ciphers:
            s = 0
            ctext = HextoRaw(ctext.strip())
            score, key, message = single_key_Xor(ctext, possible_keys)
            L.append((score, message))
    print sorted(L, reverse=True)[0][1]



#print scores()
