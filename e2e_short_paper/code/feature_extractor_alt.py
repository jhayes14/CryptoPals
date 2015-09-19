#import re
import collections
from operator import sub

def flow_volume_total(data, number_chunks=40):
    last_packet = data[-1]
    last_time = last_packet.split()[0]
    splits = float(last_time)/number_chunks
    split_list = []
    for i in range(1,number_chunks+1):
        split_list.append(splits*i)
    time_flow = []
    for packets in data:
        packet_time = float(packets.split()[0])
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

def flow_volume_in(data):
    in_flow = []
    for packet in data:
        if float(packet.split("\t")[1]) == -1:
            in_flow.append(packet)
        else:
            pass
    return flow_volume_total(in_flow)

def flow_volume_out(data):
    out_flow = []
    for packet in data:
        if float(packet.split("\t")[1]) == 1:
            out_flow.append(packet)
        else:
            pass
    return flow_volume_total(out_flow)

def composite_flow_volume(flow_volume):
    f = flow_volume
    #dictlist = []
    #for k, v in f.items():
    #    temp = [k,v]
    #    dictlist.append(temp)
    l = []
    for prev,item,next in neighborhood(f):
        l.append([item[0], item[1] - prev[1]])
    return l


def neighborhood(iterable):
    iterator = iter(iterable)
    prev = [0,0]
    item = iterator.next()  # throws StopIteration if empty.
    for next in iterator:
        yield (prev,item,next)
        prev = item
        item = next
    yield (prev,item,None)


def extract_features(data, site, instance):
    fname = str(site) + "-" + str(instance)

    #Extract features. All features are non-negative numbers or X.
    features = []
    features.append(flow_volume_total(data))
    features.append(flow_volume_in(data))
    features.append(flow_volume_out(data))
    features.append(composite_flow_volume(flow_volume_total(data)))
    features.append(composite_flow_volume(flow_volume_in(data)))
    features.append(composite_flow_volume(flow_volume_out(data)))

    fout = open("../data/batch/" + fname + "f", "w")
    for x in features:
        fout.write(repr(x) + " ")
    fout.close()


#-------------------------

if __name__ == "__main__":
    tcp_dump = open("../data/batch/2-81").readlines()
    for site in range(0, 1):
        for instance in range(0, 2):
            extract_features(tcp_dump, site, instance)
