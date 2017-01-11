"""
    https://cryptopals.com/sets/1/challenges/3
"""

from cryptofuncs import *

if __name__ == "__main__":
    input_str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    cipher = HextoRaw(input_str)
    possible_keys = [x for x in range(256)]
    score, key, message = single_key_Xor(cipher, possible_keys)
    print "Key:", key
    print "Message:", message
