import distance
import cPickle
import random
import math

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
 

def get_successes_temp(h1, h2, nu = 9000):
    if os.path.exists('../data/nearest_hash_dump_use.p'):
        data = cPickle.load(open('../data/nearest_hash_dump_use.p', 'rb'))
        print len(data)
        web_lmt = 90
        count = 0
        match = 0
        perfect = 0
        number_zeros = 0
        print "hash number - (hamming distance, nearest hash number)"
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
        print "number of perfect (out of %s) hash and alt hash matches: %s" % (nu, perfect)
        print "perfect = %s" %(perfect/float(nu))
        print "number of correct (out of %s) website assignments: %s" %(nu, match)
        print "match = %s" %(match/float(nu))
        print "average number of zero hamming distances: %s" %(number_zeros/float(nu))
        base_rate = (number_zeros/float(nu))/(nu/float(90))
        if base_rate > 1:
            print "base rate success = %d" %(1.0)
        else:
            print "base rate success = %s" %(base_rate)
        print

        return base_rate, perfect/float(nu), match/float(nu)
        #elif len(data) <= nu:
        #    print "not enough data"
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
        cPickle.dump(nearest_hash_dump, open('../data/nearest_hash_dump_use.p', 'wb'))

data = cPickle.load(open('../data/nearest_hash_info.p', 'rb'))
for n in range(10):
    #for _ in range(10):
    perfect_score = 0
    website_score = 0
    for _ in range(1000):
        random.shuffle(data)
        for item in data[:n]:
            if item[0] == item[2][0][1]:
                perfect_score += 1
                
    print n+1, perfect_score/float(20*(n+1))




"""total_new = []
for item in data:
    print item[0]
    dists = []
    for ele in item[1]:
        ele = ele 
        b = [math.floor(ele[1]/float(90))]
        new = list(ele) + b
        dists.append(tuple(new))
    site = math.floor(item[0]/float(90))    
    total_new.append((item[0], site, dists))
cPickle.dump(total_new, open('../data/nearest_hash_info.p', 'wb'))""" 
