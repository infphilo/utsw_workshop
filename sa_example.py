#!/usr/bin/env python

import sys

# Read a part of the human chromosome sequences, 10,000-bp long
seq = ""
for line in open("22_10K.fa"):
    if line.startswith('>'):
        continue
    line = line.strip()
    line = line.replace('N', '')
    seq += line


# Create an array of suffixes
sa = range(len(seq))


# Print the first 100 unsorted suffixes
for seq_i in sa[:100]:
    print "%6d" % seq_i, seq[seq_i:seq_i+100] # Print the first 100 bases of a suffix


# Sort suffixes
def compare_suffixes(a, b):
    seq_a = seq[a:]
    seq_b = seq[b:]

    if seq_a < seq_b:
        return -1
    elif seq_a == seq_b:
        return 0
    else:
        return 1


sa = sorted(sa, cmp=compare_suffixes)


# Print the first 100 sorted suffixes
for seq_i in sa[:100]:
    print "%6d" % seq_i, seq[seq_i:seq_i+100] # Print the first 100 bases of a suffix


# Read 100 reads
reads = []
for line in open("reads.fa"):
    line = line.strip()
    if line.startswith('>'):
        read_name, read_pos = line[1:].split()
    else:
        read_seq = line
        reads.append([read_name, int(read_pos), read_seq])


# Perform alignment of reads using a binary search algorithm
def binary_search(seq, sa, read_seq):
    l, r = 0, len(sa)
    while l < r:
        m = (l + r) / 2
        seq_m = sa[m]
        cmp_seq = seq[seq_m:seq_m+len(read_seq)]
        if read_seq == cmp_seq:
            return seq_m
        elif read_seq < cmp_seq:
            r = m
        else:
            l = m + 1
            
    return -1

for read_name, read_pos, read_seq in reads:
    aligned_read_pos = binary_search(seq, sa, read_seq)
    assert read_pos == aligned_read_pos

print "Passed!"
    
    
