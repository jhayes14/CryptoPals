""" 
    https://cryptopals.com/sets/1/challenges/1
"""

from cryptofuncs import *


if __name__ == "__main__":
    
    # First convert hex to raw
    input_str = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    raw_str = HextoRaw(input_str) 
    # Now encode to base64
    b64_str = Rawtobase64(raw_str)
    assert b64_str == "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
