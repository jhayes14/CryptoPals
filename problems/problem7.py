from cryptofuncs import *


if __name__ == "__main__":
    with open('../inputs/7.txt') as c:
        f = c.read()
        cipher = base64toRaw(f)
        key = b"YELLOW SUBMARINE"
        print ECB_decrypt(cipher, key)

