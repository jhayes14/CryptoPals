import base64
import binascii
from itertools import cycle
from Crypto.Cipher import AES
import random
import os
import string

letterFrequency = {}
letterFrequency['A'] = .082
letterFrequency['B'] = .015
letterFrequency['C'] = .028
letterFrequency['D'] = .043
letterFrequency['E'] = .127
letterFrequency['F'] = .022
letterFrequency['G'] = .020
letterFrequency['H'] = .061
letterFrequency['I'] = .070
letterFrequency['J'] = .002
letterFrequency['K'] = .008
letterFrequency['L'] = .040
letterFrequency['M'] = .024
letterFrequency['N'] = .067
letterFrequency['O'] = .075
letterFrequency['P'] = .019
letterFrequency['Q'] = .001
letterFrequency['R'] = .060
letterFrequency['S'] = .063
letterFrequency['T'] = .091
letterFrequency['U'] = .028
letterFrequency['V'] = .010
letterFrequency['W'] = .023
letterFrequency['X'] = .001
letterFrequency['Y'] = .020
letterFrequency['Z'] = .001
letterFrequency[' '] = .200


def HextoRaw(data):
    return binascii.unhexlify(data)

def RawtoHex(data):
    return binascii.hexlify(data)

def base64toRaw(data):
    return base64.b64decode(data)

def Rawtobase64(data):
    return base64.b64encode(data)

def Xor(s1, s2):
    """ operates on raw bytes """
    return ''.join([chr(ord(x) ^ ord(y)) for x,y in zip(s1, cycle(s2))])

def single_key_Xor(ciphertext, possible_keys):
    candidates = [ ]
    for key in possible_keys:
        key = chr(key)
        longkey = key * len(ciphertext)
        longkey = longkey[:len(ciphertext)]
        plaintext = Xor(ciphertext, longkey)
        score = 0
        for char in plaintext.upper():
            if char in letterFrequency:
                score += letterFrequency[char]
        candidates.append((score, key, plaintext))
    return sorted(candidates, reverse=True)[0]


def transpose_ciphertext(ciphertext, keylen):
    trans = []
    for i in range(keylen):
        trans.append(ciphertext[i::keylen])
    return trans


def hamming_distance(s1,s2):
    if len(s1)==len(s2):
        s = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
    else:
        return False
    bits = 0
    if s: # they are in fact the same length
        for c in s:
            bits += sum(bit == '1' for bit in bin(ord(c))[2:])
        return bits
    else:
        return False

def tryKey(cipher, key):
    fullkey = key * len(cipher)
    fullkey = fullkey[:len(cipher)]
    potential_plain = Xor(HextoRaw(cipher), HextoRaw(fullkey))
    if len(potential_plain) != 200:
        while len(potential_plain) < 200:
            potential_plain = "0" + potential_plain
    score = 0
    for char in potential_plain.upper():
        if char in letterFrequency:
            score += letterFrequency[char]
    return score, potential_plain

def find_key_size(data):
    n = len(data)
    min_key_size = 100
    for i in range(2,40):
        candidate = []
        for j in range(int(n/i-1)):
            dist = hamming_distance(data[i*j:i*(j+1)], data[i*(j+1):i*2*j])/float(i)
            candidate.append(dist)
        cand = sum(candidate)
        if cand < min_key_size:
            min_key_size = cand
            best = (i, cand)
    return best[0]


def findKey(data, key_size):
    trans_cipher = transpose_ciphertext(data, key_size)
    key = ""
    trans_hex_cipher = [RawtoHex(x) for x in trans_cipher]
    for block in trans_hex_cipher:
        best_mscore = 0.0
        best_key = 0
        for i in range(256):
            mscore, plaintext = tryKey(block, hex(i)[2:])
            if (mscore > best_mscore):
                best_mscore = mscore
                best_key = i
        key += chr(best_key)
    return str(key)

def ECB_decrypt(cipher, key):
    """ operates on bytes """
    res = AES.new(key, AES.MODE_ECB)
    return res.decrypt(cipher)

def ECB_encrypt(plain, key):
    """ operates on bytes """
    if len(plain)%16 != 0:
        plain = pkcs7_pad_alt(plain, 16)
    res = AES.new(key, AES.MODE_ECB)
    return res.encrypt(plain)

def detect_ECB(text):
    '''
    Detect ECB mode. If the text has a repeated block, it means
    that the plaintext was likely using ECB mode.
    '''
    block_length = 16
    blocks = [text[i*block_length:block_length*(i+1)] for i in range(int(len(text)/block_length))]
    if len(set(blocks)) != len(blocks):
        return True
    else:
        return False

def pkcs7_pad(text, length):
    result = bytearray(text)
    remainder = length - (len(text) % length)
    result += bytearray([remainder]*remainder)
    return result

def pkcs7_pad_alt(text, length):
    remainder = length - len(text) % length
    return text + chr(remainder) * remainder

def encrypt_AES_CBC(plain, key, IV):
    """ Decrypt a cipher text using AES
        CBC with ECB mode. Operates on bytes.
    """
    if len(plain) % 16 != 0:
        raise ValueError('Cipher must be a multiple of blocks of length 16')
    ciphertext = []
    block = [plain[i*len(key):(i+1)*len(key)] for i in range(int(len(plain) / len(key)))]
    for i in range(int(len(plain) / len(key))):
        if i > 0:
            xored = Xor(block[i], ciphertext[i-1])
        elif i == 0:
            xored = Xor(block[i], IV)
        encrypted = ECB_encrypt(xored, key)
        ciphertext.append(encrypted)
    return "".join(ciphertext)

def decrypt_AES_CBC(cipher, key, IV):
    """ Decrypt a cipher text using AES
        CBC with ECB mode. Operates on bytes.
    """
    if len(cipher) % 16 != 0:
        raise ValueError('Cipher must be a multiple of blocks of length 16')
    plaintext = []
    block = [cipher[i*len(key):(i+1)*len(key)] for i in range(int(len(cipher) / len(key)))]
    for i in range(int(len(cipher) / len(key))):
        decrypted = ECB_decrypt(block[i], key)
        if i > 0:
            xored = Xor(decrypted, block[i-1])
        elif i == 0:
            xored = Xor(decrypted, IV)
        plaintext.append(xored)
    return "".join(plaintext)

def generate_AES_key():
    """ generate random 16 byte AES key """
    #print binascii.hexlify(os.urandom(16))
    return randomword(16)

def generate_AES_key_alt(strlen):
    return ''.join(map(chr,[random.randint(0, 255) for _ in range(strlen)]))

def encryption_oracle(plaintext, debug=False):
    """ encrypt using CBC or ECB (random choice) """
    key = generate_AES_key()
    modes = ['ECB', 'CBC']
    mode = random.choice(modes)
    if debug:
        print(mode)
    prepend = randomword(random.randrange(5,10))
    append = randomword(random.randrange(5,10))
    plain = ''.join((prepend, plaintext, append))

    if mode == 'ECB':
        padded_plain = pkcs7_pad(plain, 16)
        padded_plain, key = RawtoHex(padded_plain), RawtoHex(key)
        encrypted = ECB_encrypt(padded_plain, key)
    elif mode == 'CBC':
        iv = generate_AES_key()
        padded_plain = pkcs7_pad(plain, 16)
        padded_plain, iv, key = RawtoHex(padded_plain), RawtoHex(iv), RawtoHex(key)
        #encrypted = encrypt_AES_CBC(str(padded_plain), str(key), str(iv))
        encrypted = encrypt_AES_CBC(padded_plain, key, iv)
    return encrypted, mode

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def ECB_oracle(plaintext, secret, key):
    blocksize = 16
    plaintext = pkcs7_pad_alt(plaintext + base64toRaw(secret), blocksize)
    ciphertext = ECB_encrypt(plaintext, key)
    return ciphertext

def detect_cipher_block_size(ciphertext, key):
    attack_plain = 'A'
    for i in range(1000):
        data = RawtoHex(pkcs7_pad(attack_plain, 16))
        data = HextoRaw(data)
        encrypted = ECB_encrypt(data, key)
        if len(encrypted) > len(ciphertext):
            #print "Block size is %d" %(len(encrypted) - len(ciphertext))
            return len(encrypted) - len(ciphertext)
        else:
            attack_plain += "A"
    print "Not found"

def to_append(string, blocksize):
    needappend = blocksize - len(string) % blocksize - 1
    return needappend * 'A'

def parser(Obj):
    P = {}
    obj = Obj.split("&")
    for item in obj:
        split_item = item.split("=")
        P[split_item[0]] = split_item[1]
    return P

def profile_for(obj):
    email = ''.join([x for x in obj if x!='='])
    email = ''.join([x for x in email if x!='&'])
    uid = 10
    role = 'user'
    return 'email=' + email + '&uid=' + str(uid) + '&role=' + role

def find_prefix_length(prefix, secret, key):
    for i in range(0, 16*3):
        ciphertext = ECB_oracle(prefix + (i * 'A'), secret, key)
        for b in range(len(ciphertext)/16 - 1):
            if ciphertext[(b+1)*16:(b+2)*16] == ciphertext[(b+2)*16:(b+3)*16]:
                return 16*3 - i + 16 * b
    return 0

def find_secret_length(prefix, secret, key):
    ciphertext = ECB_oracle(prefix, secret, key)
    total_len = len(ciphertext)
    blocklen = detect_cipher_block_size(ciphertext, key)
    prefix_len = find_prefix_length(prefix, secret, key)
    for i in range(blocklen + 1):
        if total_len < len(ECB_oracle(prefix + (i * 'A'), secret, key)):
            return total_len - i - prefix_len

def is_valid_pkcs7(text):
    #padded_plain = pkcs7_pad_alt(text, length)
    last_char_int = int(RawtoHex(text[-1]), 16)
    split_pad = [int(RawtoHex(x), 16) for x in text[-last_char_int:]]
    if all(i==last_char_int for i in split_pad) and text[-last_char_int-1]!=last_char_int:
        return text
    else:
        raise Exception("Invalid PKCS#7 padding!")
