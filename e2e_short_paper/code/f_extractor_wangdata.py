#This extracts timing features from the wang et al data set.
import numpy as np
import math
#wang et al features
# WANG DATA --> -1 corresponds to an incoming packet and 1 corresponds to an outgoing packet

#creates even sized sublists of a list
def chunkIt(seq, num):
  avg = len(seq) / float(num)
  out = []
  last = 0.0
  while last < len(seq):
    out.append(seq[int(last):int(last + avg)])
    last += avg
  return out

#Gives list of inter packet times from original list
def inter_pckt_time(lst):
    Dt = [y[0] - x[0] for x, y in zip(lst[:-1], lst[1:])]
    return Dt

#Splits data in to original data, just the the in packets, and just the outpackets
def InOutTotal(data):
    Total = []
    for pkt in data:
        p = pkt.split("\t")
        p0 = float(p[0])
        p1 = float(p[1])
        Total.append((p0, p1))
    In = []
    Out = []
    for p in Total:
        if p[1] == -1:
            In.append(p)
        if p[1] == 1:
            Out.append(p)
    return In, Out, Total

#Gives the inter packets times of the total data, the In packets, and the Out packets
def interarrival_times(inout_data):
    In, Out, Total = inout_data
    IN = inter_pckt_time(In)
    OUT = inter_pckt_time(Out)
    TOTAL = inter_pckt_time(Total)
    return IN, OUT, TOTAL

#For original, In and Out packets this gives inter arrival time stats such as mean arrival time, std dev time etc.
def interarrival_maxminmeansd_stats(inout_data):
    interstats = []
    In, Out, Total = interarrival_times(inout_data)
    if In and Out:
        avg_in = sum(In)/float(len(In))
        avg_out = sum(Out)/float(len(Out))
        avg_total = sum(Total)/float(len(Total))
        interstats.append([max(In), max(Out), max(Total), avg_in, avg_out, avg_total, np.std(In), np.std(Out), np.std(Total), np.percentile(In, 75), np.percentile(Out, 75), np.percentile(Total, 75)])
    elif Out and not In:
        avg_out = sum(Out)/float(len(Out))
        avg_total = sum(Total)/float(len(Total))
        interstats.append([0, max(Out), max(Total), 0, avg_out, avg_total, 0, np.std(Out), np.std(Total), 0, np.percentile(Out, 75), np.percentile(Total, 75)])
    elif In and not Out:
        avg_in = sum(In)/float(len(In))
        avg_total = sum(Total)/float(len(Total))
        interstats.append([max(In), 0, max(Total), avg_in, 0, avg_total, np.std(In), 0, np.std(Total), np.percentile(In, 75), 0, np.percentile(Total, 75)])
    else:
        interstats.extend([0]*15)
    return interstats

#For orignial, In, Out data returns the statistics about the total transmission times
def time_percentile_stats(inout_data):
    In, Out, Total = inout_data
    In1 = [x[0] for x in In]
    Out1 = [x[0] for x in Out]
    Total1 = [x[0] for x in Total]
    STATS = []
    if In1:
        STATS.append(np.percentile(In1, 25)) # return 25th percentile
        STATS.append(np.percentile(In1, 50)) #
        STATS.append(np.percentile(In1, 75)) #
        STATS.append(np.percentile(In1, 100)) #
    if not In1:
        STATS.extend(([0]*4))
    if Out1:
        STATS.append(np.percentile(Out1, 25)) # return 25th percentile
        STATS.append(np.percentile(Out1, 50)) #
        STATS.append(np.percentile(Out1, 75)) #
        STATS.append(np.percentile(Out1, 100))
    if not Out1:
        STATS.extend(([0]*4))
    if Total1:
        STATS.append(np.percentile(Total1, 25)) # return 25th percentile
        STATS.append(np.percentile(Total1, 50))
        STATS.append(np.percentile(Total1, 75))
        STATS.append(np.percentile(Total1, 100))
    if not Total1:
        STATS.extend(([0]*4))
    return STATS

#Number of packets in orginal, In and Out data
def number_pkt_stats(inout_data):
    In, Out, Total = inout_data
    return len(In), len(Out), len(Total)

#Number of In and Out packets in the first and last 30 packets
def first_and_last_30_pkts_stats(inout_data):
    In, Out, Total = inout_data
    first30 = Total[:30]
    last30 = Total[-30:]
    first30in = []
    first30out = []
    for p in first30:
        if p[1] == -1:
            first30in.append(p)
        if p[1] == 1:
            first30out.append(p)
    last30in = []
    last30out = []
    for p in last30:
        if p[1] == -1:
            last30in.append(p)
        if p[1] == 1:
            last30out.append(p)
    stats= []
    stats.append(len(first30in))
    stats.append(len(first30out))
    stats.append(len(last30in))
    stats.append(len(last30out))
    return stats

#concentration of outgoing packets in chunks of 20 packets
def pkt_concentration_stats(inout_data):
    In, Out, Total = inout_data
    chunks= [Total[x:x+20] for x in xrange(0, len(Total), 20)]
    concentrations = []
    for item in chunks:
        c = 0
        for p in item:
            if p[1] == 1:
                c+=1
        concentrations.append(c)
    return np.std(concentrations), sum(concentrations)/float(len(concentrations)), np.percentile(concentrations, 50), min(concentrations), max(concentrations), concentrations
    #return sum(concentrations)/float(len(concentrations))
    #return concentrations


#Average number packets sent and received per second
def number_per_sec(inout_data):
    In, Out, Total = inout_data
    last_time = Total[-1][0]
    last_second = math.ceil(last_time)

    l = [0] * int(last_second)
    for time, _ in Total:
        l[int(math.floor(time))] += 1


    # print l
    avg_number_per_sec = sum(l)/float(len(l))
    return np.mean(l), np.std(l), np.percentile(l, 50), min(l), max(l), l


#Packet ordering features from http://cacr.uwaterloo.ca/techreports/2014/cacr2014-05.pdf
def avg_pkt_ordering_stats(inout_data):
    In, Out, Total = inout_data

    c1 = 0
    c2 = 0
    temp1 = []
    temp2 = []
    for p in Total:
        if p[1] == 1:
            temp1 += [c1]
        c1+=1
        if p[1] == -1:
            temp2 += [c2]
        c2+=1
    avg_in = sum(temp1)/float(len(temp1))
    avg_out = sum(temp2)/float(len(temp2))

    return avg_in, avg_out, np.std(temp1), np.std(temp2)

#percentage of in and out packets as fraction of total number of packets
def perc_inc_out(inout_data):
    In, Out, Total = inout_data
    percentage_in = len(In)/float(len(Total))
    percentage_out = len(Out)/float(len(Total))
    return percentage_in, percentage_out

####################################################

#Create tuple of all of the above features, with max tuple size set at 150
def TOTAL_FEATURES(data, max_size=150):

    inout_data = InOutTotal(data)

    intertimestats = interarrival_maxminmeansd_stats(inout_data)[0]

    timestats = time_percentile_stats(inout_data)
    number_pkts = list(number_pkt_stats(inout_data))
    thirtypkts = first_and_last_30_pkts_stats(inout_data)
    stdconc, avgconc, medconc, minconc, maxconc, conc = pkt_concentration_stats(inout_data)

    avg_per_sec, std_per_sec, med_per_sec, min_per_sec, max_per_sec, per_sec = number_per_sec(inout_data)


    avg_order_in, avg_order_out, std_order_in, std_order_out = avg_pkt_ordering_stats(inout_data)
    perc_in, perc_out = perc_inc_out(inout_data)

    altconc = []
    alt_per_sec = []
    altconc = [sum(x) for x in chunkIt(conc, 20)]
    alt_per_sec = [sum(x) for x in chunkIt(per_sec, 20)]
    if len(altconc) == 20:
        altconc.append(0)
    if len(alt_per_sec) == 20:
        alt_per_sec.append(0)

    #assert len(altconc) == 21
    #assert len(alt_per_sec) == 21

    ALL_FEATURES = []
    ALL_FEATURES.extend(intertimestats)
    ALL_FEATURES.extend(timestats)
    ALL_FEATURES.extend(number_pkts)
    ALL_FEATURES.extend(thirtypkts)
    ALL_FEATURES.append(stdconc)
    ALL_FEATURES.append(avgconc)
    ALL_FEATURES.append(avg_per_sec)
    ALL_FEATURES.append(std_per_sec)
    ALL_FEATURES.append(avg_order_in)
    ALL_FEATURES.append(avg_order_out)
    ALL_FEATURES.append(std_order_in)
    ALL_FEATURES.append(std_order_out)

    #print len(ALL_FEATURES),


    #NEW
    ALL_FEATURES.append(medconc)
    ALL_FEATURES.append(med_per_sec)
    ALL_FEATURES.append(min_per_sec)
    ALL_FEATURES.append(max_per_sec)
    #ALL_FEATURES.append(minconc)
    ALL_FEATURES.append(maxconc)
    ALL_FEATURES.append(perc_in)
    ALL_FEATURES.append(perc_out)
    ALL_FEATURES.extend(altconc)
    ALL_FEATURES.extend(alt_per_sec)
    ALL_FEATURES.append(sum(altconc))
    ALL_FEATURES.append(sum(alt_per_sec))

    ALL_FEATURES.append(sum(intertimestats))
    ALL_FEATURES.append(sum(timestats))
    ALL_FEATURES.append(sum(number_pkts))


    #print len(ALL_FEATURES),


    ALL_FEATURES.extend(conc)
    #ALL_FEATURES.extend(per_sec)

    #print len(ALL_FEATURES)


    #PADPADPAD
    #print len(conc)
    #print len(per_sec)
    #print len(ALL_FEATURES)

    while len(ALL_FEATURES)<max_size:
        ALL_FEATURES.append(0)
    features = ALL_FEATURES[:max_size]
    #features = ALL_FEATURES
    return tuple(features)

#-------------------------

if __name__ == "__main__":
    for j in range(18,40):
        print "########"

        for i in range(23,24):
            tcp_dump = open("../data/batch/" + str(j) + "-" + str(i)).readlines()
            #perc_inc_out(tcp_dump)
            TOTAL_FEATURES(tcp_dump)
    for j in range(1,10):
        print j, "########"
        tcp_dump = open("../data/batch/" + str(j)).readlines()
        #perc_inc_out(tcp_dump)
        TOTAL_FEATURES(tcp_dump)
