"""
    https://cryptopals.com/sets/1/challenges/6
"""

import cryptofuncs

if __name__ == "__main__":

    with open('../inputs/6.txt','rb') as f:
            cipher = f.read().strip()

    # decode into ciphertext
    ciphertext = cryptofuncs.base64toRaw(cipher)
    key_size = cryptofuncs.find_key_size(ciphertext)
    print("KEY SIZE:", key_size)
    key = cryptofuncs.findKey(ciphertext, key_size)
    print("KEY:", key)
    print("MESSAGE:", cryptofuncs.Xor(ciphertext, key))
