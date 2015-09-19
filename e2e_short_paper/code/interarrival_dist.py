from itertools import cycle
import collections
import math
import numpy as np
import os


#path = '/Users/jamie/web_fingerprinting/data/tcp_captures_unmonitored_0_25_sanitize/'
path = '../data/batch/'

def neighborhood(iterable):
    iterator = iter(iterable)
    prev = 0
    item = iterator.next()  # throws StopIteration if empty.
    for next in iterator:
        yield (prev,item,next)
        prev = item
        item = next
    yield (prev,item,None)

def get_dist():
    total_in_int_times = []
    total_out_int_times = []
    #incoming
    for j in range(100):
        for i in range(90):
        #if os.path.exists(path + str(j) + "_EC2_1.txt"):
        #    data = open(path + str(j) + "_EC2_1.txt").readlines() 
            data = open(path + str(j) + "-" + str(i)).readlines() 
            data = [[float(text.split()[0]), float(text.split()[1])] for text in data]
            in_times = [x[0] for x in data if x[1] == -1]
            out_times = [x[0] for x in data if x[1] == 1]
        
            #print in_times
            in_int_times = []
            out_int_times = []
            #for pkt in in_data:
        
            for prev,item,next in neighborhood(in_times):
                in_int_times.append(item - prev)
            total_in_int_times.extend(in_int_times)
            for prev,item,next in neighborhood(out_times):
                out_int_times.append(item - prev)
            total_out_int_times.extend(out_int_times)


    total_in_int_times = sorted(total_in_int_times)
    total_out_int_times = sorted(total_out_int_times)

    t_sep = []
    for i in (10**(-n) for n in xrange(7)):
        t_sep.append(i)
    t_sep.extend((0.5, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100))
    t_sep = sorted(t_sep)

    total_pkts = []
    total_pkts_out = []

    for t in t_sep:
        c1=0
        for i in total_in_int_times:
            if i == 0:
                pass
            elif i <= t:
                c1+=1
        total_pkts.append(c1) 
        c2=0
        for i in total_out_int_times:
            if i == 0:
                pass
            elif i <= t:
                c2+=1
        total_pkts_out.append(c2) 


    t_p  = []
    t_p_out = []
    for prev,item,next in neighborhood(total_pkts):
        t_p.append(item - prev)
    for prev,item,next in neighborhood(total_pkts_out):
        t_p_out.append(item - prev)
    
    return t_sep, t_p, t_p_out

