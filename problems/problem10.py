from cryptofuncs import *

if __name__ == "__main__":
    
    with open('../inputs/10.txt') as c:
        cipher = c.read()
        cipher = base64toRaw(cipher)
        key = 'YELLOW SUBMARINE'
        #IV = binascii.unhexlify('%02d' % 0) * len(key)
        IV = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        print "".join(decrypt_AES_CBC(cipher,key, IV))

