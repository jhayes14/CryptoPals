"""
    https://cryptopals.com/sets/1/challenges/5
"""

from cryptofuncs import *

if __name__ == "__main__":
    key = "ICE"
    plain = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
    
    print RawtoHex(Xor(plain, key))
