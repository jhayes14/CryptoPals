
def obfuscate(data, pct_keep = 99):
    new_flow = []
    for packet in data:
        x = random.randint(0,100)
        if x <= pct_keep:
            new_flow.append(packet)
    temp = []
    for f in new_flow:
        timestamp = f.split("\t")[0]
        new_timestamp = float(timestamp) + float(laplace(random.randint(-30,30), 0, 10))
        temp.append([new_timestamp,float(f.split("\t")[1])])

    #WRITE OUT NEW FILE
    return temp




get_alt_hashes(compute_hash(composite_flow_volume(flow_volume_total_alt(obfuscate(tcp_dump)))), file="../data/e2ehashes_randsin_alt-1pctdrp__50chunks_512bits.txt")
