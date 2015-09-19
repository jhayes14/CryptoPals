import random
import numpy as np
import os
import argparse
import feature_extractor
import feature_extractor_alt
import pickle
import compute_hash

sites = 100
instances = 90

def laplace(x, mu, b):
    """http://en.wikipedia.org/wiki/Laplace_distribution"""
    return 1.0/(2*b) * np.exp(-abs(x - mu)/b)

def obfuscate_traces(pkt_keep=50):
    for j in range(sites):
        print j
        for i in range(instances):
            data = open("../data/batch/" + str(j) + "-" + str(i)).readlines()
            new_flow = []
            for packet in data:
                x = random.randint(0,100)
                if x <= pkt_keep:
                    new_flow.append(packet)
            temp = []
            for f in new_flow:
                timestamp = f.split("\t")[0]
                new_timestamp = float(timestamp) + float(laplace(random.randint(-30,30), 0, 10))
                temp.append([new_timestamp,float(f.split("\t")[1])])
            directory = "../data/batch_%d_pkt_drop/" %(100-pkt_keep)
            if not os.path.exists(directory):
                os.makedirs(directory)
            thefile = open(directory + str(j) + "-" + str(i), 'w')
            for item in temp:
                thefile.write("%s %s\n" % (item[0], item[1]))
            thefile.close()

def extract_features(traces, chunks=10):
    features = {'feature_data': [],
                 'feature_label': []}

    for i in range(sites):
        print i
        for j in range(instances):
            # print i, j
            fname = str(i) + "-" + str(j)
            tcp_dump = open(traces + fname).readlines()
            g = []
            if traces == '../data/batch/':
                g.append(feature_extractor.flow_volume_total(tcp_dump, number_chunks=chunks))
                g.append(feature_extractor.composite_flow_volume(feature_extractor.flow_volume_total(tcp_dump, number_chunks=chunks)))
            else:
                g.append(feature_extractor_alt.flow_volume_total(tcp_dump, number_chunks=chunks))
                g.append(feature_extractor_alt.composite_flow_volume(feature_extractor_alt.flow_volume_total(tcp_dump, number_chunks=chunks)))
            features['feature_data'].append(g)
            features['feature_label'].append((i,j))

    assert len(features['feature_data']) == len(features['feature_label'])
    fileObject = open(traces + 'features_' + 'chunks_' + str(chunks),'wb')
    pickle.dump(features,fileObject)
    fileObject.close()

def generate_rand_vals(direc):
    """Generate random numbers for sampling later - Range variable depending on hash length"""
    master_list = []
    for i in range(1024):
        rand_vals = []
        for j in range(i):
            rand_vals.append(random.uniform(-1,1))
        master_list.append(rand_vals)
    fileObject = open(direc + 'rand_vals','wb')
    pickle.dump(master_list,fileObject)
    fileObject.close()


def get_hashes(features, f, hash_length):
    fileObject1 = open(features,'r')
    F = pickle.load(fileObject1)
    #print F['feature_data'][1][1]
    #print F['feature_label'][1]
    if os.path.isfile(f):
        os.remove(f)

    for i, data in enumerate(F['feature_data']):
        #print i
        #compute_hash.compute_hash(data[0]) #total volume flow
        hash_lst = compute_hash.compute_hash(data[1], L=hash_length) #composite volume flow
        with open(f, "a") as thefile:
                thefile.write("%s %s\n" % (hash_lst, F['feature_label'][i]))
        thefile.close()



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='E2E correlation experiments')
    parser.add_argument('--obfuscate_traces', action='store_true', help='write obfuscated traces to file.')
    parser.add_argument('--extract_features', action='store_true', help='extract feature traces to file.')
    parser.add_argument('--generate_rand_vals', action='store_true', help='Generate random numbers for sampling later - Range variable depending on hash length.')
    parser.add_argument('--get_hashes', action='store_true', help='write hashes to file.')

    parser.add_argument('--pkt_keep', nargs=1, metavar="INT", help='Percent of packets to keep.')
    parser.add_argument('--traces', nargs=1, metavar="STR", help='Directory of traces for feature extraction.')
    parser.add_argument('--chunks', nargs=1, metavar="INT", help='Number of chunks a trace is split in to.')
    parser.add_argument('--hash_length', nargs=1, metavar="INT", help='Hash length.')

    args = parser.parse_args()

    if args.obfuscate_traces:
        # Example command line:
        # $ python create_hashes.py --obfuscate_traces --pkt_keep 1
        pkt_keep = int(args.pkt_keep[0])
        obfuscate_traces(pkt_keep)

    if args.extract_features:
        # Example command line:
        # $ python create_hashes.py --extract_features --traces ../data/batch/ --chunks 10
        traces = str(args.traces[0])
        chunks = int(args.chunks[0])
        extract_features(traces, chunks)

    if args.generate_rand_vals:
        # Example command line:
        # $ python create_hashes.py --generate_rand_vals
        direc = '../data/'
        generate_rand_vals(direc)

    if args.get_hashes:
        # Example command line:
        # $ python create_hashes.py --get_hashes --traces ../data/batch/features_chunks_10 --hash_length 256
        traces = str(args.traces[0])
        hash_length = int(args.hash_length[0])
        f = traces + '_' + str(hash_length) + '_hash_length_' + 'hashes.txt'
        get_hashes(traces, f, hash_length)
