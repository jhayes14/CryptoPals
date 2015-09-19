import pickle
import graph_compare_hashes

total = []
for i in [10, 50, 100]: #chunks
    for j in [64, 128, 256]: #hash length
        for _ in range(3):
            h1 = '../data/batch/features_chunks_' + str(i) + '_' + str(j) + '_hash_length_hashes.txt'
            h2 = '../data/batch_' + str(1) + '_pkt_drop/features_chunks_' + str(i) + '_' + str(j) + '_hash_length_hashes.txt'
            c, match_rate = graph_compare_hashes.fig_lsh_website_matches(h1,h2,j)
            total.append(match_rate)


fileObject = open('../data/batch_' + str(1) + '_pkt_drop/variables_lsh_website_matches','wb')
pickle.dump(total,fileObject)
fileObject.close()

total5 = []
for i in [10, 50, 100]: #chunks
    for j in [64, 128, 256]: #hash length
        for _ in range(3):
            h1 = '../data/batch/features_chunks_' + str(i) + '_' + str(j) + '_hash_length_hashes.txt'
            h2 = '../data/batch_' + str(5) + '_pkt_drop/features_chunks_' + str(i) + '_' + str(j) + '_hash_length_hashes.txt'
            c, match_rate = graph_compare_hashes.fig_lsh_website_matches(h1,h2,j)
            total5.append(match_rate)


fileObject = open('../data/batch_' + str(5) + '_pkt_drop/variables_lsh_website_matches','wb')
pickle.dump(total5,fileObject)
fileObject.close()


total10 = []
for i in [10, 50, 100]: #chunks
    for j in [64, 128, 256]: #hash length
        for _ in range(3):
            h1 = '../data/batch/features_chunks_' + str(i) + '_' + str(j) + '_hash_length_hashes.txt'
            h2 = '../data/batch_' + str(10) + '_pkt_drop/features_chunks_' + str(i) + '_' + str(j) + '_hash_length_hashes.txt'
            c, match_rate = graph_compare_hashes.fig_lsh_website_matches(h1,h2,j)
            total10.append(match_rate)


fileObject = open('../data/batch_' + str(10) + '_pkt_drop/variables_lsh_website_matches','wb')
pickle.dump(total10,fileObject)
fileObject.close()






