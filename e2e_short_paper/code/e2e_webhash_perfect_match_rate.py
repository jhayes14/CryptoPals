#we consider a positive match if alt has is 0 hamm dist and failure otherwise

#- say on average how many other flows had 0 hamm dist

import random
import re
from random import randint, shuffle
import decimal
import numpy as np
import matplotlib.pylab as plt
import matplotlib.pyplot as plot
import matplotlib as mpl
import matplotlib.patches as mpatches
import math
from operator import add
import distance
import os
import line_profiler
import e2elocalhash
import feature_extractor
#import seaborn as sns
import cPickle

"binary hash comparison for websites - uses e2elocalhash.py as a base script"



# ------ Generate random numbers for sampling later - Range variable depending on hash length  ----

rand_vals_128 = []
for j in range(0,128):
    rand_vals_128.append(random.uniform(-1,1))

rand_vals_256 = []
for j in range(0,256):
    rand_vals_256.append(random.uniform(-1,1))

rand_vals_512 = []
for j in range(0,512):
    rand_vals_512.append(random.uniform(-1,1))

# -------------------------------------------------------------------------------------------------

def laplace(x, mu, b):
    """http://en.wikipedia.org/wiki/Laplace_distribution"""
    return 1.0/(2*b) * np.exp(-abs(x - mu)/b)

def extract_features(data, CHUNKS=10):
    #Extract features. All features are non-negative numbers or X.
    features = []
    features.append(feature_extractor.flow_volume_total(data, number_chunks=CHUNKS))
    features.append(feature_extractor.flow_volume_in(data))
    features.append(feature_extractor.flow_volume_out(data))
    features.append(feature_extractor.composite_flow_volume(feature_extractor.flow_volume_total(data, number_chunks=CHUNKS)))
    features.append(feature_extractor.composite_flow_volume(feature_extractor.flow_volume_in(data)))
    features.append(feature_extractor.composite_flow_volume(feature_extractor.flow_volume_out(data)))

    total_flow = features[0]
    total_in = features[1]
    total_out = features[2]
    comp_flow = features[3]
    comp_in = features[4]
    comp_out = features[5]

    #return total_flow, total_in, total_out, comp_flow, comp_in, comp_out
    return total_flow, comp_flow


def compute_hash(flow, L=256, rand_vals = rand_vals_256):
    'compute hash of random flow segment'
    H = [0]*L                  #Initialize projection values H1, H2, ..., HL
    h_value = []
    comp_flow = flow
    for i in range(len(comp_flow)):
        if i==0:
            flowStart =  comp_flow[i][0]       #first packet timestamp is when the flow starts
        elif i > 0:
            T_bar = float(comp_flow[i][0]) - float(flowStart) #relative timestamp
            B_bar = float(comp_flow[i][1]) - float(comp_flow[i-1][1]) #difference in bitrate
            temp = []
            for j in range(L):
                #projection = math.sin(T_bar + j)*math.tan(T_bar + j)
                #projection = math.sin(T_bar + j)*math.cos(T_bar + j)
                projection = math.sin(T_bar + j)/5 + math.sin((T_bar + j)*rand_vals[j])*rand_vals[j]
                temp.append(projection)
            second_temp = [i * B_bar for i in temp]
            H = map(add, H, second_temp)
    for proj in H:
        if proj > 0:
            h_value.append(1)
        elif proj <= 0:
            h_value.append(0)
    return h_value

def graph_projections():
    #sns.set_style("whitegrid")
    sns.set_style("ticks")
    sns.set_context("paper")

    xs = np.linspace(0, 50, num=2048)
    ys = [math.sin(j)*math.tan(j) for j in xs]
    zs = [math.sin(x)*math.cos(x) for x in xs]

    #two examples of pseudorandom functions
    ws = [(math.sin(x)/5 + math.sin((x)*rand_vals[0])*rand_vals[0]) for x in xs]
    vs = [(math.sin(x)/5 + math.sin((x)*rand_vals[-1])*rand_vals[-1]) for x in xs]

    #plot.plot(xs, ys)
    #plot.plot(xs, zs)
    plot.plot(xs, ws)
    plot.plot(xs, vs)

    plot.show()




def get_hashes(hash_lst, file="e2ehashes.txt"):
    with open(file, "a") as thefile:
            thefile.write("%s\n" % hash_lst)
    thefile.close()

def get_obfuscated_features(lst, pct_keep = 99):
    new_flow = []
    for packet in lst:
        x = random.randint(0,100)
        if x <= pct_keep:
            new_flow.append(packet)
    new_flow_time = []
    new_flow_size = []
    for trace in new_flow:
        timestamp = re.findall(r'\S+', trace)[0]
        new_timestamp = float(timestamp) + float(laplace(random.randint(-30,30), 0, 10))
        new_flow_time.append(new_timestamp)
        number_bytes = re.findall(r'\S+', trace)[-1]
        new_flow_size.append(number_bytes)
        #print number_bytes
    return len(new_flow_time), new_flow_time, new_flow_size

def composite_flow_volume(flow_volume):
    f = flow_volume
    l = []
    for prev,item,next in feature_extractor.neighborhood(f):
        l.append([item[0], item[1] - prev[1]])
    return l


def obfuscate(data, pct_keep = 99):
    new_flow = []
    for packet in data:
        x = random.randint(0,100)
        if x <= pct_keep:
            new_flow.append(packet)
    temp = []
    for f in new_flow:
        timestamp = f.split("\t")[0]
        new_timestamp = float(timestamp) + float(laplace(random.randint(-30,30), 0, 10))
        temp.append([new_timestamp,float(f.split("\t")[1])])
    return temp


def flow_volume_total_alt(lst, CHUNKS=50):
    last_packet = lst[-1]
    last_time = last_packet[0]
    splits = float(last_time)/CHUNKS
    split_list = []
    for i in range(1,CHUNKS+1):
        split_list.append(splits*i)
    time_flow = []
    for packets in lst:
        packet_time = float(packets[0])
        time_flow.append(packet_time)
    #feature_dict = collections.OrderedDict()
    flow_features = []
    for s in split_list:
        temp = []
        for t in time_flow:
            if t < s:
                temp.append(t)
        #feature_dict[s] = len(temp)
        flow_features.append([s, len(temp)])
    return flow_features


def get_alt_hashes(hash_lst, file="e2ehashes_alt.txt"):
    with open(file, "a") as thefile:
            thefile.write("%s\n" % hash_lst)
    thefile.close()


def graph_boundaries(hash1, hash2, lb=0, ub=50):

    fig, ax = plt.subplots()

    for b in range(lb, ub):
        print b
        avg_dist1, tru_pos, fal_neg = e2elocalhash.compare_hashes(hash1, hash2, boundary=b)
        avg_dist2, fal_pos, tru_neg = e2elocalhash.compare_random_hashes(hash1, hash2, boundary=b)
        ax.scatter(b, tru_pos, color='r', label="True positive")
        ax.scatter(b, fal_pos, color='b', label="False positive")
        #ax.scatter(b, fal_neg, color='g', label="False negative")
        #ax.scatter(b, tru_neg, color='y', label="True negative")


    red_patch = mpatches.Patch(color='red', label='The red data')
    blue_patch = mpatches.Patch(color='blue', label='The blue data')

    plt.legend([red_patch, blue_patch], ["True positive", "False positive"])

    plt.xlabel('boundary')
    plt.ylabel('%')
    #plt.show()
    #plt.savefig('../results/e2ecorrelation_rate_sintan.pdf', format="pdf", transparent=True, bbox_inches='tight',)
    #plt.savefig('../results/e2ecorrelation_rate_sincos.pdf', format="pdf", transparent=True, bbox_inches='tight',)
    plt.savefig('../results/e2ecorrelation_rate_randsin.pdf', format="pdf", transparent=True, bbox_inches='tight',)

def find_nearest_hash(hsh, hash_doc):
    temp = []
    for i, h in enumerate(hash_doc):
        hamm_dist = distance.hamming(hsh, h)
        temp.append((hamm_dist, i))
    return min(temp, key=lambda x: x[0])

def find_nearest_x_hashes(hsh, hash_doc, x=100):
    temp = []
    for i, h in enumerate(hash_doc):
        hamm_dist = distance.hamming(hsh, h)
        temp.append((hamm_dist, i))
    return sorted(temp, key=lambda x: x[0])[:x]
    #average = sum(n for _, n in temp[:x])
    #return min(temp, key=lambda x: x[0])

#cycle through hashes and check if the min hamm corresponds to the correct alt_hash
#this needs to get success for correct web page assignment i.e. if hash and nearest hash are the same webpage (with +-90 of each other!)
def get_successes(h1, h2, nu=20):
    if os.path.exists('../data/nearest_hash_dump.p'):
        data = cPickle.load(open('../data/nearest_hash_dump.p', 'rb'))
        print len(data)

        if len(data) > nu:
            web_lmt = 90
            count = 0
            match = 0
            perfect = 0
            print "Hash number - (Hamming distance, Nearest Hash number)"
            for i in range(nu):
                if (web_lmt-90)<=count<=web_lmt:
                    if (web_lmt-90)<=data[i][1]<=web_lmt:
                        match += 1
                    print count, data[i]
                    if data[i][1] == count:
                        perfect += 1
                    count += 1
                elif count>web_lmt:
                    web_lmt = web_lmt + 90
            print
            print "Number of perfect (out of %s) hash and alt hash matches: %s" % (nu, perfect)
            print "Number of correct (out of %s) website assignments: %s" %(nu, match)
            print
        elif len(data) <= nu:
            print "Not enough data"
    else:
        with h1 as f:
            nearest_hash_dump = []
            for i, x in enumerate(f):
                if i in range(nu):
                    near_hash = find_nearest_hash(x, h2)
                    print near_hash
                    nearest_hash_dump.append(near_hash)
                else:
                    break
        cPickle.dump(nearest_hash_dump, open('../data/nearest_hash_dump.p', 'wb'))






def get_successes_TEMP(h1, h2, nu = 9000):
    if os.path.exists('../data/nearest_hash_dump_USE.p'):
        data = cPickle.load(open('../data/nearest_hash_dump_USE.p', 'rb'))
        print len(data)
        web_lmt = 90
        count = 0
        match = 0
        perfect = 0
        number_zeros = 0
        print "Hash number - (Hamming distance, Nearest Hash number)"
        for i in range(nu):
            if (web_lmt-90)<=count<web_lmt:
                data_r = [(dist, name) for dist, name in data[i] if (dist == 0 and (web_lmt-90)<=name<web_lmt)]
                data_k = [(dist, name) for dist, name in data[i] if (dist == 0 and name<nu)]
                if data_r:
                    #print count, data[i]
                    if (0, count) in data_r:
                        perfect += 1
                    if any((web_lmt-90)<=y<web_lmt for (x,y) in data_r):
                        match += 1
                if data_k:
                    number_zeros += len(data_k)
                else:
                    pass
                count += 1

            elif count>=web_lmt:
                web_lmt = web_lmt + 90
                data_r = [(dist, name) for dist, name in data[i] if (dist == 0 and (web_lmt-90)<=name<web_lmt)]
                data_k = [(dist, name) for dist, name in data[i] if (dist == 0 and name<nu)]
                if data_r:
                    #print count, data[i]
                    if (0, count) in data_r:
                        perfect += 1
                    if any((web_lmt-90)<=y<web_lmt for (x,y) in data_r):
                        match += 1
                    number_zeros += len(data_r)
                if data_k:
                    number_zeros += len(data_k)
                else:
                    pass
                count += 1
        print
        print "Number of perfect (out of %s) hash and alt hash matches: %s" % (nu, perfect)
        print "perfect = %s" %(perfect/float(nu))
        print "Number of correct (out of %s) website assignments: %s" %(nu, match)
        print "match = %s" %(match/float(nu))
        print "Average number of zero hamming distances: %s" %(number_zeros/float(nu))
        base_rate = (number_zeros/float(nu))/(nu/float(90))
        if base_rate > 1:
            print "Base rate success = %d" %(1.0)
        else:
            print "Base rate success = %s" %(base_rate)
        print

        return base_rate, perfect/float(nu), match/float(nu)
        #elif len(data) <= nu:
        #    print "Not enough data"
    else:
        with h1 as f:
            nearest_hash_dump = []
            for i, x in enumerate(f):
                if i in range(nu):
                    near_hash = find_nearest_x_hashes(x, h2)
                    print
                    print i, near_hash
                    print
                    nearest_hash_dump.append(near_hash)
                else:
                    break
        cPickle.dump(nearest_hash_dump, open('../data/nearest_hash_dump_USE.p', 'wb'))


def graph_diff_success():
    fig, ax = plt.subplots()
    c = 1
    b = []
    p = []
    m = []
    for i in range(90, 9090, 90):
        print "-----"
        print "Number of websites %s" %c
        base_rate, perfect, match = get_successes_TEMP(nu = i)
        b.append(base_rate)
        p.append(perfect)
        m.append(match)
        c+=1

    ax.plot(range(1, c), b, color='b', label="Base")
    ax.plot(range(1, c), p, color='r', label="Perfect")
    ax.plot(range(1, c), m, color='g', label="Success")


    plt.legend(loc='best')

    plt.xlabel('Number of websites')
    plt.ylabel('Match fraction')

    plt.show()
    #plt.savefig('../results/e2ecorrelation_rate_total_50chunks_256bits_1pctdrp.pdf', format="pdf", transparent=True, bbox_inches='tight',)





#------------------------- # timing tests ------ #
if __name__ == "__main__":

    #    for j in range(0,90):
    #        fname = str(i) + "-" + str(j)
    #        tcp_dump = open("../data/batch/" + fname).readlines()
    #        get_hashes(compute_hash(extract_features(tcp_dump)), file="../data/e2ehashes_randsin-1pctdrp_50chunks_512bits.txt")
    #        get_alt_hashes(compute_hash(composite_flow_volume(flow_volume_total_alt(obfuscate(tcp_dump)))), file="../data/e2ehashes_randsin_alt-1pctdrp__50chunks_512bits.txt")

    # ---- sin-tan projection ----------------------

    #hashes1 = open("../data/e2ehashes_sintan.txt").readlines()
    #alt_hashes1 = open("../data/e2ehashes_sintan_alt.txt").readlines()
    #e2elocalhash.compare_hashes(hashes1, alt_hashes1, boundary=50)
    #e2elocalhash.compare_random_hashes(hashes1, alt_hashes1, boundary=50)
    #graph_boundaries(hashes1, alt_hashes1)

    #h1 = open("../data/e2ehashes_sintan.txt", 'r')
    #get_successes(h1, alt_hashes1, nu=30) #9000 max

    # ---- sin-cos projection ----------------------

    #hashes2 = open("../data/e2ehashes_sincos.txt").readlines()
    #alt_hashes2 = open("../data/e2ehashes_sincos_alt.txt").readlines()
    #e2elocalhash.compare_hashes(hashes2, alt_hashes2, boundary=10)
    #e2elocalhash.compare_random_hashes(hashes2, alt_hashes2, boundary=10)
    #graph_boundaries(hashes2, alt_hashes2)

    #h2 = open("../data/e2ehashes_sincos.txt", 'r')
    #get_successes(h2, alt_hashes2, nu=9000)

    # ---- random pick projection ----------------------
    #hashes3 = open("../data/e2ehashes_randsin_%s_%dchunks_%dbits.txt").readlines() %("total", 10, 256)
    #alt_hashes3 = open("../data/e2ehashes_ALT_randsin_%s_%dchunks_%dbits_%dpctdrp.txt" %("total", 10, 256, 1)).readlines()
    #e2elocalhash.compare_hashes(hashes3, alt_hashes3, boundary=3)
    #e2elocalhash.compare_random_hashes(hashes3, alt_hashes3, boundary=3)
    #graph_boundaries(hashes3, alt_hashes3, lb=0, ub=150)

    #h3 = open("../data/e2ehashes_randsin_%s_%schunks_%sbits.txt" %("total", 50, 256), 'r')
    #graph_diff_success(h3, alt_hashes3)
    #h1 = open("../data/USE_hashes_randsin_%dchunks_%dbits.txt" %(50, 256), 'r')
    #h2 = open("../data/USE_hashes_randsin_alt_%spctdrp_%schunks_%sbits.txt" %(1, 50, 256)).readlines()
    #get_successes_TEMP(h1, h2, nu = 9000)

    #######################################################

    #graph_projections()
    graph_diff_success()


    #------------PROFILER--------------------------

    #profiler = line_profiler.LineProfiler()
    #profiler.add_function(get_successes)
    #profiler.run('get_successes(h3, alt_hashes3, nu=20)')
    #profiler.print_stats()

#TODO 1. alongside normal results, check if the alt hash is the matched up against its true hash! - strong result! -
#     2. GRAPH RESULTS WITH SEABORN -
#     3. analyse effect of choice of pseudorandom functions
#     4. Use time and size not just time
