from cryptofuncs import *


SECRET = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
KEY = generate_AES_key()

def get_block_size():
    cipher = ECB_oracle('', SECRET, KEY)
    return detect_cipher_block_size(cipher, KEY)

def val_ECB():
    key = generate_AES_key()
    plaintext = generate_AES_key() * 2
    ciphertext_b = ECB_oracle(plaintext, SECRET, KEY)
    print "ECB mode:", detect_ECB(ciphertext_b)

def make_dict(data, blocksize):
	lbdict = {}
	for i in range(0, 256):
		blockcipher = ECB_oracle(data + chr(i), SECRET, KEY)
		lbdict[blockcipher[0:len(data)+1]] = i
	return lbdict


def find_secret(blocksize):
    knownstring = ''
    while True:
        needtoappend = to_append(knownstring, blocksize)
        data = needtoappend + knownstring
        lbdict = make_dict(data, blocksize)	# ECB_oracle( data || for-character || unknown-string )
        samplecipher = ECB_oracle(needtoappend, SECRET, KEY)[0:len(data)+1]  # ECB_oracle( data || unknown-string )
        if samplecipher in lbdict:
            rc = chr(lbdict[samplecipher])
            knownstring += rc
        else:
            return knownstring
    return knownstring

if __name__ == '__main__':
    blocksize = get_block_size()
    val_ECB()
    print 'SECRET string:', find_secret(blocksize)
