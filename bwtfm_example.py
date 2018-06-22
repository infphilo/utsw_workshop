#!/usr/bin/env python

# Read a part of the human chromosome sequences, 10,000-bp long
seq = ""
for line in open("22_10K.fa"):
    if line.startswith('>'):
        continue
    line = line.strip()
    line = line.replace('N', '')
    seq += line


# Add '$' to the end of the sequence
seq += '$'


# Create an array of suffixes
sa = range(len(seq))


# Print the first 100 unsorted suffixes
for seq_i in sa[:100]:
    suffix = seq[seq_i:seq_i+100]
    if seq_i + 100 > len(seq):
        suffix += seq[:(seq_i + 100) % len(seq)]

    print "%6d" % seq_i, suffix # Print the first 100 bases of a suffix

    
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
print "\n"
for seq_i in sa[:100]:
    suffix = seq[seq_i:seq_i+100]
    if seq_i + 100 > len(seq):
        suffix += seq[:(seq_i + 100) % len(seq)]
    
    print "%6d" % seq_i, suffix # Print the first 100 bases of a suffix

A_count, C_count, G_count, T_count = seq.count('A'), seq.count('C'), seq.count('G'), seq.count('T')
assert 1 + A_count + C_count + G_count + T_count == len(seq)

F = {'$' : 0, 'A' : 1, 'C' : 1 + A_count, 'G' : 1 + A_count + C_count , 'T' : 1 + A_count + C_count + G_count}
L = [seq[(seq_i - 1 + len(seq)) % len(seq)] for seq_i in sa]
POS = [seq_i for seq_i in sa]


# Perform alignment of reads using BWT
def align_bwt(F, L, POS, read_seq):
    top, bot = 0, len(L)

    def LF(F, L, top, bot, nt):
        new_top = F[nt] + L[:top].count(nt)
        new_bot = F[nt] + L[:bot].count(nt)

        return new_top, new_bot

    for nt in read_seq[::-1]:
        top, bot = LF(F, L, top, bot, nt)
        assert top < bot

    if top < bot:
        # Take the first one, though there might be multiple locations for the given sequence
        return POS[top] 

    else:
        return -1


# Store positions at every 16th suffix
POS_16 = [sa[i] for i in range(0, len(sa), 16)]

# Build count tables for every 100 nucleotides
FM_100 = []
for i in range(0, len(L), 100):
    counts = {'$' : 0, 'A' : 0, 'C' : 0, 'G' : 0, 'T' : 0}
    for nt in L[i:i+100]:
        counts[nt] += 1

    if len(FM_100) > 0:
        for nt, count in FM_100[-1].items():
            counts[nt] += count
    FM_100.append(counts)

# Perform alignment of reads using BWT/FM index
def align_bwtfm(F, L, POS, read_seq):
    top, bot = 0, len(L)

    def LF(F, L, top, bot, nt):
        top_i = top / 100
        add_top = FM_100[top_i-1][nt] if top_i > 0 else 0

        top_from = top_i * 100
        new_top = F[nt] + add_top + L[top_from:top].count(nt)

        bot_i = bot / 100
        add_bot = FM_100[bot_i-1][nt] if bot_i > 0 else 0
                
        bot_from = bot_i * 100
        new_bot = F[nt] + add_bot + L[bot_from:bot].count(nt)

        return new_top, new_bot

    def LF_one(F, L, top):
        nt = L[top]

        top_i = top / 100
        add_top = FM_100[top_i-1][nt] if top_i > 0 else 0

        top_from = top_i * 100
        new_top = F[nt] + add_top + L[top_from:top].count(nt)

        return new_top

    for nt in read_seq[::-1]:
        top, bot = LF(F, L, top, bot, nt)
        assert top < bot

    if top < bot:
        shift = 0
        while top % 16 != 0:
            top = LF_one(F, L, top)
            shift += 1

        return (POS_16[top / 16] + shift) % len(seq)

    else:
        return -1



# Read 100 reads
reads = []
for line in open("reads.fa"):
    line = line.strip()
    if line.startswith('>'):
        read_name, read_pos = line[1:].split()
    else:
        read_seq = line
        reads.append([read_name, int(read_pos), read_seq])


for read_name, read_pos, read_seq in reads:
    aligned_read_pos = align_bwt(F, L, POS, read_seq)
    assert read_pos == aligned_read_pos

    aligned_read_pos = align_bwtfm(F, L, POS, read_seq)
    assert read_pos == aligned_read_pos


print "Passed!"
    
    
