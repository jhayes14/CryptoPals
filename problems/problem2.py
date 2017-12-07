"""
    https://cryptopals.com/sets/1/challenges/2
"""
from cryptofuncs import *

if __name__ == "__main__":
    
    hex_a = "1c0111001f010100061a024b53535009181c"
    hex_b = "686974207468652062756c6c277320657965"
    print RawtoHex(Xor(HextoRaw(hex_a), HextoRaw(hex_b)))
