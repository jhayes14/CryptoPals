from cryptofuncs import *

def solve():
    with open('../inputs/8.txt') as C:
        for line in C:
            if detect_ECB(line):
                print "ECB:", line

if __name__ == "__main__":
    solve()
