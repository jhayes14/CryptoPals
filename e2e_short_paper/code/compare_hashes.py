import distance
import argparse
from lshash import LSHash
import ast
import random

import numpy
from nearpy import Engine
from nearpy.hashes import RandomBinaryProjections

instances = 90

def splitter(l, n):
    """ Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def perfect_matches(hashdoc, obfs_hashdoc, test_num = 100):
    hashdoc = open(hashdoc).readlines()
    obfs_hashdoc = open(obfs_hashdoc).readlines()
    c = list(zip(hashdoc, obfs_hashdoc))
    random.shuffle(c)
    hashdoc, obfs_hashdoc = zip(*c)
    assert len(hashdoc) == len(obfs_hashdoc)
    p = 0
    for j, hsh in enumerate(hashdoc[:test_num]):
        print j
        hsh = hsh.split(' (')[0]
        temp = []
        for i, h in enumerate(obfs_hashdoc[:test_num]):
            h = h.split(' (')[0]
            hamm_dist = distance.hamming(hsh, h)
            temp.append((hamm_dist, i))
        top_x = sorted(temp, key=lambda x: x[0])[:10]
        #print j, top_x
        #average = sum(n for _, n in temp[:x])
        if top_x[0][1] == j:
            p+=1
    return p/float(test_num)

# using lshash
def lsh_perfect_matches(hashdoc, obfs_hashdoc, test_num = 100, hash_l = 256):
    hashdoc = open(hashdoc).readlines()
    obfs_hashdoc = open(obfs_hashdoc).readlines()
    c = list(zip(hashdoc, obfs_hashdoc))
    random.shuffle(c)
    hashdoc, obfs_hashdoc = zip(*c)
    assert len(hashdoc) == len(obfs_hashdoc)
    lsh = LSHash(40, hash_l, num_hashtables=50)
    for j, hsh in enumerate(hashdoc[:test_num]):
        #print j
        hsh = hsh.split(' (')[0]
        hsh = ast.literal_eval(hsh)
        lsh.index(hsh, extra_data=j)
    c = 0
    for i, h in enumerate(obfs_hashdoc[:test_num]):
        h = h.split(' (')[0]
        h = ast.literal_eval(h)
        #print i, lsh.query(h)
        #print i
        try:
            if lsh.query(h)[0][0][1] == i:
                c +=1
        except IndexError:
            pass
    return c/float(test_num)

# using nearpy
#def lsh_matches(hashdoc, obfs_hashdoc):
#    hashdoc = open(hashdoc).readlines()
#    obfs_hashdoc = open(obfs_hashdoc).readlines()
#    dimension = 256
#    rbp = RandomBinaryProjections('rbp', 20)
#    engine = Engine(dimension, lshashes=[rbp])
#    for j, hsh in enumerate(hashdoc):
#        print j
#        hsh = hsh.split(' (')[0]
#        hsh = ast.literal_eval(hsh)
#        hsh = numpy.array(hsh)
#        engine.store_vector(hsh, j)
#    c = 0
#    for i, h in enumerate(obfs_hashdoc):
#        h = h.split(' (')[0]
#        h = ast.literal_eval(h)
#        h = numpy.array(h)
#        print i
#        try:
#            if engine.neighbours(h)[0][1] == i:
#                c +=1
#        except IndexError:
#            pass
#    print c/float(len(hashdoc))

def website_matches(hashdoc, obfs_hashdoc, test_num = 100):
    hashdoc = open(hashdoc).readlines()
    obfs_hashdoc = open(obfs_hashdoc).readlines()
    assert len(hashdoc) == len(obfs_hashdoc)
    split_hashdoc = list(splitter(hashdoc, instances))
    split_obfs_hashdoc = list(splitter(obfs_hashdoc, instances))
    c = list(zip(split_hashdoc, split_obfs_hashdoc))
    random.shuffle(c)
    split_hashdoc, split_obfs_hashdoc = zip(*c)

    #de-split
    hashdoc = [item for sublist in split_hashdoc for item in sublist]
    obfs_hashdoc = [item for sublist in split_obfs_hashdoc for item in sublist]
    p = 0
    for j, hsh in enumerate(hashdoc[:test_num]):
        print j
        label = ast.literal_eval(hsh.split('] ')[1])
        hsh = hsh.split(' (')[0]
        #label = hsh.split(' (')[0]
        temp = []
        for i, h in enumerate(obfs_hashdoc[:test_num]):
            obfs_label = ast.literal_eval(h.split('] ')[1])
            h = h.split(' (')[0]
            hamm_dist = distance.hamming(hsh, h)
            temp.append((hamm_dist, obfs_label))
        top_x = sorted(temp, key=lambda x: x[0])[:10]
        #print j, top_x
        #average = sum(n for _, n in temp[:x])
        if top_x[0][1][0] == label[0]:
            p+=1
    return p/float(test_num)

def lsh_website_matches(hashdoc, obfs_hashdoc, test_num = 100, hash_l = 256):
    hashdoc = open(hashdoc).readlines()
    obfs_hashdoc = open(obfs_hashdoc).readlines()
    assert len(hashdoc) == len(obfs_hashdoc)
    split_hashdoc = list(splitter(hashdoc, instances))
    split_obfs_hashdoc = list(splitter(obfs_hashdoc, instances))
    c = list(zip(split_hashdoc, split_obfs_hashdoc))
    random.shuffle(c)
    split_hashdoc, split_obfs_hashdoc = zip(*c)

    #de-split
    hashdoc = [item for sublist in split_hashdoc for item in sublist]
    obfs_hashdoc = [item for sublist in split_obfs_hashdoc for item in sublist]
    lsh = LSHash(40, hash_l, num_hashtables=50)
    for j, hsh in enumerate(hashdoc[:test_num]):
        #print j
        label = ast.literal_eval(hsh.split('] ')[1])
        hsh = hsh.split(' (')[0]
        hsh = ast.literal_eval(hsh)
        lsh.index(hsh, extra_data=label)

    c = 0
    for i, h in enumerate(obfs_hashdoc[:test_num]):
        #print i
        obfs_label = ast.literal_eval(h.split('] ')[1])
        h = h.split(' (')[0]
        h = ast.literal_eval(h)
        #print i, lsh.query(h)
        try:
            if lsh.query(h)[0][0][1][0] == obfs_label[0]:
                c +=1
        except IndexError:
            pass
    return c/float(test_num)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='E2E correlation experiments')
    parser.add_argument('--perfect_matches', action='store_true', help='Compare hashes for perfect matching.')
    parser.add_argument('--lsh_perfect_matches', action='store_true', help='Compare hashes for lsh perfect matching.')
    parser.add_argument('--website_matches', action='store_true', help='Compare hashes for website matching.')
    parser.add_argument('--lsh_website_matches', action='store_true', help='Compare hashes for lsh website matching.')

    parser.add_argument('--pkt_drop', nargs=1, metavar="INT", help='%\ of packets dropped.')
    parser.add_argument('--chunks', nargs=1, metavar="INT", help='Number of chunks.')
    parser.add_argument('--hash_length', nargs=1, metavar="INT", help='hash length.')
    parser.add_argument('--test_num', nargs=1, metavar="INT", help='Number to test.')

    args = parser.parse_args()

    if args.perfect_matches:
        # Example command line:
        # $ python compare_hashes.py --perfect_matches --pkt_drop 10 --chunks 10 --hash_length 256 --test_num 10

        pkt_drop = int(args.pkt_drop[0])
        chunks = int(args.chunks[0])
        hash_length = int(args.hash_length[0])
        test_num = int(args.test_num[0])

        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'

        perfect_matches(h1,h2,test_num)

    if args.lsh_perfect_matches:
        # Example command line:
        # $ python compare_hashes.py --lsh_perfect_matches --pkt_drop 10 --chunks 10 --hash_length 256 --test_num 10

        pkt_drop = int(args.pkt_drop[0])
        chunks = int(args.chunks[0])
        hash_length = int(args.hash_length[0])
        test_num = int(args.test_num[0])

        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'

        lsh_perfect_matches(h1,h2, test_num, hash_length)

    if args.website_matches:
        # Example command line:
        # $ python compare_hashes.py --website_matches --pkt_drop 10 --chunks 10 --hash_length 256 --test_num 10

        pkt_drop = int(args.pkt_drop[0])
        chunks = int(args.chunks[0])
        hash_length = int(args.hash_length[0])
        test_num = int(args.test_num[0])

        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'

        website_matches(h1,h2, test_num)

    if args.lsh_website_matches:
        # Example command line:
        # $ python compare_hashes.py --lsh_website_matches --pkt_drop 10 --chunks 10 --hash_length 256 --test_num 10

        pkt_drop = int(args.pkt_drop[0])
        chunks = int(args.chunks[0])
        hash_length = int(args.hash_length[0])
        test_num = int(args.test_num[0])

        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'

        lsh_website_matches(h1,h2, test_num, hash_length)
