import math
import os
import create_hashes, compare_hashes
import matplotlib.pylab as plt

def create_window_size(pkt_drop = 1, w_size = 0.1):
    path = "../data/batch_%d_pkt_drop/" %(pkt_drop)
    new_w_path = "../data/batch_%d_pkt_drop/w_size_%f/" %(pkt_drop, w_size)
    if not os.path.exists(new_w_path):                                                                                                                      
        os.makedirs(new_w_path)
    for j in range(100):
        print j
        for i in range(90):
            data = open(path + str(j) + "-" + str(i)).readlines()  
            #print data
            thefile = open(new_w_path + str(j) + "-" + str(i), 'w')
            for k, item in enumerate(data):
                if k <= math.ceil(len(data)*w_size):   
                    time = [float(n) for n in item.split()][0]
                    direction = [float(n) for n in item.split()][1]
                    thefile.write("%s %s\n" % (time, direction))
                else:
                    break
            thefile.close()        

def get_window_features(pkt_drop = 1, w_size = 0.1):  
    path = "../data/batch_%d_pkt_drop/w_size_%f/" %(pkt_drop, w_size) 
    create_hashes.extract_features(path, chunks = 100)


def get_window_hashes(pkt_drop = 1, w_size = 0.1):
    for i in [10, 50, 100]:
        print i
        traces = "../data/batch_%d_pkt_drop/w_size_%f/features_chunks_%d" %(pkt_drop, w_size, i)   
        for hash_length in [64, 128, 256]:
            print hash_length
            f = traces + '_' + str(hash_length) + '_hash_length_' + 'hashes.txt'
            create_hashes.get_hashes(traces, f, hash_length)


#test_num 9000 is max!
def compare_perfect_windows(pkt_drop = 1, chunks = 10, hash_length = 64, test_num = 100):
    total = [0] 
    for w_size in [x/float(20) for x in range(1, 20)]:
        print '%f' %(w_size)
        print
        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/w_size_%f/features_chunks_' %(w_size) + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt' 
        match = compare_hashes.perfect_matches(h1,h2,test_num)
        total.append(match)
    h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
    h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
    match = compare_hashes.perfect_matches(h1,h2,test_num)
    total.append(match)
    plt.plot(total)
    plt.ylabel('Match score')
    plt.xlabel('Fraction of total window')
    xlabels = [x/float(20) for x in range(21)]
    xlabelsnew = []
    for i in xlabels:
            if i not in [x/float(10) for x in range(11)]:
                i = ' '
                xlabelsnew.append(i)
            else:
                xlabelsnew.append(i)
    plt.xticks(range(21),xlabelsnew)
    plt.savefig('../results/perfect_var_window_size_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_' + str(pkt_drop) + '_pct_drp.pdf', format="pdf", transparent=True, bbox_inches='tight',) 

def compare_website_windows(pkt_drop = 1, chunks = 10, hash_length = 64, test_num = 100):
    total = [0] 
    for w_size in [x/float(20) for x in range(1, 20)]:
        print '%f' %(w_size)
        print
        h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
        h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/w_size_%f/features_chunks_' %(w_size) + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt' 
        match = compare_hashes.website_matches(h1,h2,test_num)
        total.append(match)
    h1 = '../data/batch/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
    h2 = '../data/batch_' + str(pkt_drop) + '_pkt_drop/features_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_hashes.txt'
    match = compare_hashes.website_matches(h1,h2,test_num)
    total.append(match)
    plt.plot(total)
    plt.ylabel('Match score')
    plt.xlabel('Fraction of total window')
    xlabels = [x/float(20) for x in range(21)]
    xlabelsnew = []
    for i in xlabels:
            if i not in [x/float(10) for x in range(11)]:
                i = ' '
                xlabelsnew.append(i)
            else:
                xlabelsnew.append(i)
    plt.xticks(range(21),xlabelsnew)
    plt.savefig('../results/website_var_window_size_chunks_' + str(chunks) + '_' + str(hash_length) + '_hash_length_' + str(pkt_drop) + '_pct_drp.pdf', format="pdf", transparent=True, bbox_inches='tight',) 


#compare_website_windows(pkt_drop = 1, chunks = 10, hash_length = 64, test_num = 10)
compare_perfect_windows(pkt_drop = 1, chunks = 100, hash_length = 256, test_num = 1000)
