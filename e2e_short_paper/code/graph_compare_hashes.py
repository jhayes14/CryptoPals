import pickle
import compare_hashes
import argparse
import matplotlib.pylab as plt

instances = 90

def fig_perfect_matches(h, oh):
    h_len = open(h).readlines()
    max_test = len(h_len)
    for n in range(1,max_test):
        if n%10 == 0:
            print n, compare_hashes.perfect_matches(h, oh, test_num = n)

def fig_lsh_perfect_matches(h, oh, hash_l = 256):
    h_len = open(h).readlines()
    max_test = len(h_len)
    for n in range(1,max_test):
        if n%10 == 0:
            print n, compare_hashes.lsh_perfect_matches(h, oh, test_num = n, hash_l = hash_l)

def fig_website_matches(h, oh):
    h_len = open(h).readlines()
    max_test = len(h_len)
    for n in range(1,max_test):
        if n%10 == 0:
            print n, compare_hashes.website_matches(h, oh, test_num = n)

def fig_lsh_website_matches(h, oh, hash_l = 256):
    h_len = open(h).readlines()
    max_test = len(h_len)
    match_rate = []
    c=1
    for n in range(0, max_test, instances):
        if n == 0 :
            pass
        else:
            match_frac = compare_hashes.lsh_website_matches(h, oh, test_num = n, hash_l = hash_l)
            print n, match_frac
            match_rate.append(match_frac)
            c+=1

    return c, match_rate



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='E2E correlation experiments figs')
    parser.add_argument('--fig_perfect_matches', action='store_true', help='perfect matching fig.')
    parser.add_argument('--fig_lsh_perfect_matches', action='store_true', help='lsh perfect matching fig.')
    parser.add_argument('--fig_website_matches', action='store_true', help='website matching fig.')
    parser.add_argument('--fig_lsh_website_matches', action='store_true', help='lsh website matching fig.')

    parser.add_argument('--pkt_drop', nargs=1, metavar="INT", help='%\ of packets dropped.')
    parser.add_argument('--chunks', nargs=1, metavar="INT", help='Number of chunks.')
    parser.add_argument('--hash_length', nargs=1, metavar="INT", help='hash length.')

    args = parser.parse_args()

    if args.fig_perfect_matches:
        # Example command line:
        # $ python graph_compare_hashes.py --fig_perfect_matches --pkt_drop 10 --chunks 10 --hash_length 256

        pkt_drop = int(args.pkt_drop[0])
        chunks = int(args.chunks[0])
        hash_length = int(args.hash_length[0])

        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'

        # save as pickle dump - ten rounds
        total = []
        for _ in range(50):
            c, match_rate = fig_perfect_matches(h1,h2)
            total.append(match_rate)
        fileObject = open('../data/batch_' +str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes_perfect_matches','wb')
        pickle.dump(total,fileObject)
        fileObject.close()


    if args.fig_lsh_perfect_matches:
        # Example command line:
        # $ python graph_compare_hashes.py --fig_lsh_perfect_matches --pkt_drop 10 --chunks 10 --hash_length 256

        pkt_drop = int(args.pkt_drop[0])
        chunks = int(args.chunks[0])
        hash_length = int(args.hash_length[0])

        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'

        
         # save as pickle dump - ten rounds
        total = []
        for _ in range(50):
            c, match_rate = fig_lsh_perfect_matches(h1,h2,hash_length)
            total.append(match_rate)
        fileObject = open('../data/batch_' +str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes_lsh_perfect_matches','wb')
        pickle.dump(total,fileObject)
        fileObject.close()


    if args.fig_website_matches:
        # Example command line:
        # $ python graph_compare_hashes.py --fig_website_matches --pkt_drop 10 --chunks 10 --hash_length 256

        pkt_drop = int(args.pkt_drop[0])
        chunks = int(args.chunks[0])
        hash_length = int(args.hash_length[0])

        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'

        # save as pickle dump - ten rounds
        total = []
        for _ in range(50):
            c, match_rate = fig_website_matches(h1,h2)
            total.append(match_rate)
        fileObject = open('../data/batch_' +str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes_website_matches','wb')
        pickle.dump(total,fileObject)
        fileObject.close()




    if args.fig_lsh_website_matches:
        # Example command line:
        # $ python graph_compare_hashes.py --fig_lsh_website_matches --pkt_drop 10 --chunks 10 --hash_length 256

        pkt_drop = int(args.pkt_drop[0])
        chunks = int(args.chunks[0])
        hash_length = int(args.hash_length[0])

        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'

        # save as pickle dump - ten rounds
        total = []
        for _ in range(50):
            c, match_rate = fig_lsh_website_matches(h1,h2, hash_length)
            total.append(match_rate)
        fileObject = open('../data/batch_' +str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes_lsh_website_matches','wb')
        pickle.dump(total,fileObject)
        fileObject.close()


        #c, match_rate = fig_lsh_website_matches(h1,h2, hash_length)
        #fig, ax = plt.subplots()
        #ax.plot(range(1, c), match_rate, color='r', label="lsh website match")
        #plt.legend(loc='best')
        #plt.xlabel('Number of websites')
        #plt.ylabel('Match fraction')
        #plt.savefig('../results/e2ecorrelation_rate_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_' + str(pkt_drop) + '_pct_drp.pdf', format="pdf", transparent=True, bbox_inches='tight',)
