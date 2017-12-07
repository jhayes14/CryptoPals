from cryptofuncs import *
from random import randint

SECRET = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
KEY = generate_AES_key()
PREFIX = randomword(randint(1,16))

def get_block_size():
    cipher = ECB_oracle(PREFIX, SECRET, KEY)
    return detect_cipher_block_size(cipher, KEY)

def val_ECB():
    key = generate_AES_key()
    plaintext = generate_AES_key() * 2
    ciphertext_b = ECB_oracle(plaintext, SECRET, KEY)
    print "ECB mode:", detect_ECB(ciphertext_b)

def find_secret_with_secret(prefix, secret, key, blocksize):
    ciphertext = ECB_oracle(prefix, secret, key)
    total_len = len(ciphertext)
    blocksize = detect_cipher_block_size(ciphertext, key)
    prefix_len = find_prefix_length(prefix, secret, key)
    secret_len = find_secret_length(prefix, secret, key)
    plaintext = ''
    uc = (total_len + blocksize - prefix_len - 1) * 'A'
    while len(plaintext) < secret_len:
        oracle_input = ECB_oracle(prefix + uc, secret, key)
        for i in range(127):
            test = uc + plaintext + chr(i)
            if ECB_oracle(prefix + test, secret, key)[total_len:total_len + blocksize] == oracle_input[total_len:total_len + blocksize]:
                uc = uc[1:]
                plaintext += chr(i)
                break

    return plaintext


if __name__ == '__main__':
    blocksize = get_block_size()
    val_ECB()
    print "blocksize is", blocksize
    print "Length of prefix is", find_prefix_length(PREFIX, SECRET, KEY)
    print "Length of unknown string", find_secret_length(PREFIX, SECRET, KEY)
    print 'SECRET string:', find_secret_with_secret(PREFIX, SECRET, KEY, blocksize)
