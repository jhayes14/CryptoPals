import pickle
import numpy as np
import matplotlib.pylab as plt

read_x = r'../data/features_chunks_50_128_hash_length_hashes1_pkt_drop_lsh_website_matches'


fileObject4 = open(read_x,'r')
mins = pickle.load(fileObject4)
mins = [np.mean(np.array(x)) for x in zip(*mins)]
plt.plot(mins)
plt.show()
