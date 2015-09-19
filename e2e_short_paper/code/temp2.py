import math
import numpy as np

#reverse ap path and jitter path

def get_score(site, inst, jitter_path, direct = -1, w = 5):
    appath = '../data/batch-jitter-scale-0.1/' + str(site) + '-' + str(inst)
    apdata = open(appath).readlines()
    ap = [float(item.split()[0]) for item in apdata if float(item.split()[1])==direct]
    scores = []
    for m in range(50):
        #print m      
        for n in range(10):
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
    for j in range(50):
        print j
        e = 0
        f = 0
        for i in range(10):
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

traffic_score = []
jitter_path = '../data/APbatch-l6-h9/'
traffic_score.append(total_score(5, jitter_path))
jitter_path = '../data/APbatch-l5-h7/'
traffic_score.append(total_score(5, jitter_path))
jitter_path = '../data/APbatch-l4-h8/'
traffic_score.append(total_score(5, jitter_path))
import pickle
filehandler = open("traffic_scores","wb")
pickle.dump(traffic_score,filerhandler)
filehandler.close()
import matplotlib.pylab as plt
bw_labels = ['1%%', '55%%', '100%%']
plt.bar(range(len(bw_labels)), traffic_score)
plt.xlabel('Added Traffic')
plt.ylabel('Match Rate')
plt.xticks(range(len(bw_labels)),bw_labels)
plt.savefig('../results/trafficscore.pdf', format="pdf", transparent=True, bbox_inches='tight',) 








