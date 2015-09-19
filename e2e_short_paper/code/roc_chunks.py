import distance 
import random
import matplotlib.pylab as plt
import itertools

marker = itertools.cycle(('+', '.', 'o', '*'))
for pdrop in [1, 5, 10, 30]:
    normal = open('../data/batch/features_chunks_100_256_hash_length_hashes.txt').readlines()
    alt = open('../data/batch_%s_pkt_drop/features_chunks_100_256_hash_length_hashes.txt' %(pdrop)).readlines()
    print pdrop
    print
    Truepos = []
    Falsepos = []
    for value in range(0, 25):
        if value % 10 == 0:
            print value
        TP = 0
        FP = 0
        for i, h in enumerate(normal):
            normal_hash = normal[i].split(' (')[0]
            alt_hash = alt[i].split(' (')[0]
            randomID = random.randint(0,len(normal)-1)
            random_hash = alt[randomID].split(' (')[0]
            #ID = normal[i].split('] ')[1]
            dist = distance.hamming(normal_hash, alt_hash)
            randdist = distance.hamming(normal_hash, random_hash)
            if dist <= value:
                TP += 1
            if randdist <= value:
                FP += 1
        Falsepos.append(FP/float(len(normal)))
        Truepos.append(TP/float(len(normal)))
    CFalsepos = [sum(Falsepos[:i+1]) for i in xrange(len(Falsepos))]    
    plt.plot(CFalsepos, Truepos, label = '%s%% packet drop' %(pdrop),  marker=marker.next())
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.legend(loc='best')
plt.savefig('../results/roc_pdrop_with_100chunks_256hash.pdf', format="pdf", transparent=True, bbox_inches='tight',)

















