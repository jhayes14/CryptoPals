import random
import math
import numpy as np
import os
import pickle

def laplace(x, mu, b):
    """http://en.wikipedia.org/wiki/Laplace_distribution"""
    return 1.0/(2*b) * np.exp(-abs(x - mu)/b)

def obfuscate_traces(scale):
    total_jitter = 0
    for j in range(100):
        print j
        for i in range(90):
            data = open("../data/batch/" + str(j) + "-" + str(i)).readlines()
            temp = []
            jitter = 0
            for f in data:
                timestamp = f.split("\t")[0]
                #new_timestamp = float(timestamp) + float(laplace(random.randint(-30,30), 0, 10))
                new_timestamp = float(timestamp) + float(abs(np.random.laplace(0, scale)))
                jitter += abs(float(timestamp)-float(new_timestamp))
                temp.append([new_timestamp,float(f.split("\t")[1])])
            total_jitter += jitter/float(len(data))
            directory = "../data/batch-jitter-scale-" + str(scale) + "/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            thefile = open(directory + str(j) + "-" + str(i), 'w')
            for item in sorted(temp):
                thefile.write("%s %s\n" % (item[0], item[1]))
            thefile.close()
    statistics = open(directory + 'totalstatistics', 'w')
    statistics.write("Average delay = %s " %(total_jitter/float(100*90)))
    statistics.close()



def get_score(site, inst, jitter_path, direct = -1, w = 5):
    appath = '../data/APbatch-l5-h7/' + str(site) + '-' + str(inst)
    apdata = open(appath).readlines()
    ap = [float(item.split()[0]) for item in apdata if float(item.split()[1])==direct]
    scores = []
    for m in range(100):
        #print m      
        for n in range(5):
            path = jitter_path + str(m) + '-' + str(n)
            data = open(path).readlines()
            data = [float(item.split()[0]) for item in data if float(item.split()[1])==direct]
            window = max(data[-1], ap[-1])
            window_range = range(1,int(math.ceil(window))+1)
            window_range = [x*(1/float(w)) for x in range(int(math.ceil(len(window_range)*w)+1))][1:]

            window_ap = [list(x) for x in np.split(ap,np.searchsorted(ap,window_range))][:-1]
            window_data = [list(x) for x in np.split(ap,np.searchsorted(data,window_range))][:-1]
           
            score = 0
            for k in range(len(window_range)):
                #if n==9 and m==4:
                #    print len(window_data[k]), len(window_ap[k])
                if k > int(math.ceil(data[-1])):
                    score-=1
                try:
                    if len(window_data[k]) == len(window_ap[k]):
                        score+=1
                    if len(window_data[k]) == 0 and len(window_ap[k]) == 0:
                        score-=1
                except:
                    pass

            scores.append((score,int(m),int(n)))        
    return sorted(scores,key=lambda item:item[1])        

def total_score(wsize, jitter_path):
    c = 0
    d = 0
    for j in range(100):
        if j % 20 == 0:
            print j
        e = 0
        f = 0
        for i in range(5):
            d+=1
            f+=1
            s_out = get_score(j, i, jitter_path, direct=1, w = wsize)
            s_in = get_score(j, i, jitter_path, direct=-1, w = wsize)
            temp = []
            for k in range(len(s_out)):
                temp.append((s_in[k][0]+s_out[k][0], s_in[k][1], s_in[k][2]))
            best_s = sorted(temp, reverse = True)[0]
            #print j, i, sorted(temp, reverse = True)[:10]

            if best_s[1]==j and best_s[2]==i:
                c+=1
                e+=1

        #print j, e/float(f)
        #print
    return c/float(d)

import matplotlib.pylab as plt
import itertools

def fig_var_wsize():
    marker = itertools.cycle(('+', '.', 'o', '*', 'v', '^', '<'))  
    for wsize in [0.2, 1.0, 2, 5]:
        f = open("../data/APtest_windowsize_" + str(1/float(wsize)),'rb')
        AP_file = pickle.load(f)
        w, j, s = zip(*AP_file)
        plt.plot(j, s, label = "window size = %s" %(1/float(wsize)), marker = marker.next())
    plt.xlabel('Packet delay (sec)')
    plt.ylabel('Match rate')
    plt.legend(loc='best')
    plt.savefig('../results/APscore_jitterandwsize.pdf', format="pdf", transparent=True, bbox_inches='tight',)

  

if __name__ == "__main__":
    #import line_profiler
    #jpath = '../data/batch-jitter-scale-' + str(0.05) +'/'
    #profiler = line_profiler.LineProfiler()
    #profiler.add_function(total_score)
    #profiler.add_function(get_score)
    #profiler.run('total_score(0.2,jpath)')
    #profiler.run('get_score(0,0,jpath, direct = -1, w = 0.2)')
    #profiler.print_stats()
    
    #for wsize in [0.2, 1.0, 2, 5]:
    #    print 'window size = ', 1/float(wsize)
    #    print
    #    stats = []
    #    for jscale in [x/float(20) for x in range(1,21)]:
    #        jpath = '../data/batch-jitter-scale-' + str(jscale) +'/'
    #        wjscore = total_score(wsize, jpath)
    #        print 'wsize = ', 1/float(wsize), 'jitter = ', jscale, 'score = ', wjscore
    #        stats.append((1/float(wsize), jscale, wjscore))
    #    fileObject = open('../data/APtest_windowsize_' + str(1/float(wsize)) ,'wb')
    #    pickle.dump(stats,fileObject)
    #    fileObject.close()

       
    fig_var_wsize()
    






