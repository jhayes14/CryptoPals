from cryptofuncs import *
import random


KEY = generate_AES_key()
IV = generate_AES_key()


def pad_and_CBC_encrypt(String_List):
    plaintext = random.choice(String_List)
    #pad
    if len(plaintext) % 16 != 0:
        plaintext = pkcs7_pad_alt(plaintext, 16)
    #encrypt
    return encrypt_AES_CBC(plaintext, KEY, IV)

def padding_oracle(ciphertext):
    plaintext = decrypt_AES_CBC(ciphertext, KEY, IV)
    last_char_int = int(RawtoHex(plaintext[-1]), 16)
    split_pad = [int(RawtoHex(x), 16) for x in plaintext[-last_char_int:]]
    if all(i==last_char_int for i in split_pad) and plaintext[-last_char_int-1]!=last_char_int:
        return True
    else:
        return False

def xorstr(s1, s2):
    """
    FROM: set2/challenge10
    """

    def xor(c1, c2):
        return chr(ord(c1) ^ ord(c2))

    return ''.join([xor(s1[i], s2[i]) for i in range(len(s1))])

def blocks(ciphertext):
    block_length = 16
    blocks = [ciphertext[i*block_length:block_length*(i+1)] for i in range(int(len(ciphertext)/block_length))]
    return blocks


def attack(ciphertext):
    block_length = 16
    cipher_blocks = [ciphertext[i*block_length:block_length*(i+1)] for i in range(int(len(ciphertext)/block_length))]
    prev_block = IV
    plaintext = ''
    for block in cipher_blocks:
        # for valid padding, after decryption but before XOR, plaintext from attack
        attack_block, mid_block, plaintext_block = bytearray(16), bytearray(16), bytearray(16)
        for byteid in range(block_length-1, -1, -1):
            # Num of bytes for needed for valid padding
            padding = abs(block_length-byteid)
            for i in range(byteid + 1, 16):
                attack_block[i] = mid_block[i] ^ padding
            for i in range(256):
                attack_block[byteid] = i
                if padding_oracle(str(attack_block) + block):
                    break
            mid_block[byteid] = i ^ padding
            plaintext_block[byteid] = mid_block[byteid] ^ ord(prev_block[byteid])
        plaintext += ''.join(map(chr, plaintext_block))
        prev_block = block
    return plaintext

if __name__ == "__main__":

    SList = [  "MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
                "MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
                "MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
                "MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
                "MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
                "MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
                "MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
                "MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
                "MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
                "MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93" ]


    print base64toRaw(attack(pad_and_CBC_encrypt(SList)))
