#!/usr/bin/env python

# Read a part of the human chromosome sequences, 10,000-bp long
seq = ""
for line in open("22_10K.fa"):
    if line.startswith('>'):
        continue
    line = line.strip()
    line = line.replace('N', '')
    seq += line

# Print reads at every 100bp
for i in range(0, len(seq) / 100):
    print ">%d %d" % (i + 1, i * 100)
    print seq[i*100:i*100+100]

