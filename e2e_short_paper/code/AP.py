import interarrival_dist
import random
import numpy as np
import math
import os

Ltuner = 3 
Htuner = 9
print Ltuner, Htuner
#time, incount, outcount = interarrival_dist.get_dist()

#print time
#print incount
#print outcount
time = [10**-6, 10**-5, 0.0001, 0.001, 0.01, 0.1, 0.5, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 100]
incount = [1, 322, 93470, 1141632, 606318, 1077390, 264469, 32263, 5429, 2598, 2245, 1140, 538, 267, 81, 54, 32, 40, 86]
outcount = [15, 1680, 5490, 43331, 76814, 284152, 319425, 46340, 8713, 3052, 2144, 987, 564, 309, 93, 65, 65, 57, 122]
incount = [x*100 for x in incount]
outcount = [x*100 for x in outcount]

LBStime = time[1:Ltuner]
LBSin = incount[1:Ltuner]
LBSout = outcount[1:Ltuner]
HBStime = time[Htuner:]
HBSin = incount[Htuner:]
HBSout = outcount[Htuner:]


#THIS IS MISLABELLED AS IN. IT IS OUTGOING TRAFFIC
def AP(path, direct = 1):    
    data = open("../data/batch/" + str(j) + "-" + str(i)).readlines()
    data = [float(packet.split()[0]) for packet in data if float(packet.split()[1])==direct]
    #in_data = [float(packet.split()[0]) for packet in data]
    int_times = []
    for prev,item,next in interarrival_dist.neighborhood(data):
        int_times.append(item - prev)
    #out_data = [float(packet.split()[0]) for packet in data if float(packet.split()[1])==-1]
    gaptime = list(LBStime)
    bursttime = list(HBStime)
    if direct == 1:
        gaptokens = list(LBSout)
        gapprobs = [x/float(sum(gaptokens)) for x in gaptokens]
        bursttokens = list(HBSout)
        burstprobs = [x/float(sum(bursttokens)) for x in bursttokens]
    elif direct == -1:
        gaptokens = list(LBSin)
        gapprobs = [x/float(sum(gaptokens)) for x in gaptokens]
        bursttokens = list(HBSin)
        burstprobs = [x/float(sum(bursttokens)) for x in bursttokens]
    
    new_in = [0]
    gapmode = False
    for k, pkt in enumerate(data):
        if gapmode == True:
            #select random time from gap
            random_bucket = np.random.choice(gaptokens, p=gapprobs) 
            random_bucket_index = gaptokens.index(random_bucket)
            random_time = gaptime[random_bucket_index]
            r_time = random.uniform(random_time/float(10), random_time)
            #remove token and update probs 
            gaptokens = [random_bucket-1 if x==random_bucket else x for x in gaptokens]
            gapprobs = [x/float(sum(gaptokens)) for x in gaptokens]
            #print gapprobs, gaptokens
            while new_in[-1] + r_time < data[k]:
                #print "gapmode"
                new_in.append(new_in[-1]+r_time)
                #select random time from gap
                random_bucket = np.random.choice(gaptokens, p=gapprobs) 
                random_bucket_index = gaptokens.index(random_bucket)
                random_time = gaptime[random_bucket_index]
                r_time = random.uniform(random_time/float(10), random_time)
                #remove token and update probs 
                gaptokens = [random_bucket-1 if x==random_bucket else x for x in gaptokens]
                gapprobs = [x/float(sum(gaptokens)) for x in gaptokens]

            else:
                gaptokens = [random_bucket-1+1 if x==random_bucket-1 else x for x in gaptokens]
                gapprobs = [x/float(sum(gaptokens)) for x in gaptokens]
                if int_times[k] >= gaptime[-1]:
                    timecopy = list(bursttime)
                    timecopy.append(int_times[k])
                    timecopy = sorted(timecopy)
                    ind = timecopy.index(int_times[k])    
                    bursttokens = [bursttokens[ind]-1 if x==bursttokens[ind] else x for x in bursttokens]
                    burstprobs = [x/float(sum(bursttokens)) for x in bursttokens]
                    gapmode = False
                    new_in.append(data[k])
                else:    
                    timecopy = list(gaptime)
                    timecopy.append(int_times[k])
                    timecopy = sorted(timecopy)
                    ind = timecopy.index(int_times[k])    
                    gaptokens = [gaptokens[ind]-1 if x==gaptokens[ind] else x for x in gaptokens]
                    gapprobs = [x/float(sum(gaptokens)) for x in gaptokens]
                    gapmode = False
                    new_in.append(data[k])

        elif gapmode == False:
            #select random time from gap
            random_bucket = np.random.choice(bursttokens, p=burstprobs) 
            random_bucket_index = bursttokens.index(random_bucket)
            random_time = bursttime[random_bucket_index]
            r_time = random.uniform(random_time/float(10), random_time)
            #remove token and update probs 
            bursttokens = [random_bucket-1 if x==random_bucket else x for x in bursttokens]
            burstprobs = [x/float(sum(bursttokens)) for x in bursttokens]
            #print burstprobs, bursttokens
            while new_in[-1] + r_time < data[k]:
                #print "burstmode"
                gapmode = True
                new_in.append(new_in[-1]+r_time)
                random_bucket = np.random.choice(bursttokens, p=burstprobs) 
                random_bucket_index = bursttokens.index(random_bucket)
                random_time = bursttime[random_bucket_index]
                r_time = random.uniform(random_time/float(10), random_time)
                #remove token and update probs 
                bursttokens = [random_bucket-1 if x==random_bucket else x for x in bursttokens]
                burstprobs = [x/float(sum(bursttokens)) for x in bursttokens]

            else:
                bursttokens = [random_bucket-1+1 if x==random_bucket-1 else x for x in bursttokens]
                burstprobs = [x/float(sum(bursttokens)) for x in bursttokens]
                if int_times[k] >= gaptime[-1]:
                    timecopy = list(bursttime)
                    timecopy.append(int_times[k])
                    timecopy = sorted(timecopy)
                    ind = timecopy.index(int_times[k])    
                    bursttokens = [bursttokens[ind]-1 if x==bursttokens[ind] else x for x in bursttokens]
                    burstprobs = [x/float(sum(bursttokens)) for x in bursttokens]
                    new_in.append(data[k])
                else:    
                    timecopy = list(gaptime)
                    timecopy.append(int_times[k])
                    timecopy = sorted(timecopy)
                    ind = timecopy.index(int_times[k])    
                    gaptokens = [gaptokens[ind]-1 if x==gaptokens[ind] else x for x in gaptokens]
                    gapprobs = [x/float(sum(gaptokens)) for x in gaptokens]
                    new_in.append(data[k])
    new_in = new_in[1:]
    #return len(new_in)
    return new_in

       
newpath = "../data/APbatch-l%d-h%d/" %(Ltuner, Htuner)
if not os.path.exists(newpath):
    os.makedirs(newpath)
d,e = 0, 0
med = []
for j in range(50):
    f, g = 0, 0
    medpersite = []
    for i in range(10):
        d+=1
        f+=1
        path  = "../data/batch/" + str(j) + "-" + str(i)
        apadout = AP(path, direct=1)
        apadout = [(x, 1) for x in apadout]
        apadin = AP(path, direct=-1)
        apadin = [(x, -1) for x in apadin]
        pad_data = apadin + apadout
        thefile = open(newpath + str(j) + "-" + str(i), 'w')
        for item in sorted(pad_data):
            thefile.write("%s %s\n" % (item[0], item[1]))
        thefile.close()    
        
        tcpdump = open(path).readlines() 
        c1 = len([float(packet.split()[0]) for packet in tcpdump])
        c2 = len(pad_data) 
        c = c2/float(c1)
        e += c
        g += c
        med.append(c)
        medpersite.append(c)
    statistics = open(newpath + "%d_statistics" %(j), 'w')
    statistics.write("mean bandwidth = %s" %(g/float(f)))
    statistics.write("\n")
    statistics.write("median bandwidth = %s" %(np.median(np.array(medpersite))))
    statistics.close()      
print np.median(np.array(med))   
statistics = open(newpath + "totalstatistics", 'w')
statistics.write("mean bandwidth = %s" %(e/float(d)))
statistics.write("\n")
statistics.write("median bandwidth = %s" %(np.median(np.array(med))))
statistics.write("\n")
statistics.write("config: lower = 1:%d and higher=%d:" %(Ltuner,Htuner)) 
statistics.close()
