import random
import pickle
import math
from operator import add

root = '../data/rand_vals'

fileObject1 = open(root,'r')
master_list = pickle.load(fileObject1)



def compute_hash(flow, L=256):
    'compute hash of random flow segment'
    rand_vals = master_list[L]
    H = [0]*L                  #Initialize projection values H1, H2, ..., HL

    assert len(rand_vals) == len(H)

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
