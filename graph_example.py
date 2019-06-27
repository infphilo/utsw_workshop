#!/usr/bin/env python

# Implementation of HISAT2's graph index and alignment algorithms in Python for a small hypothetical genome sequence with a few variants
# Author: Daehwan Kim (infphilo@gmail.com)

# References:
# [1] Daehwan Kim, Joseph M. Paggi, Chanhee Park, Christopher Bennett, and Steven L. Salzberg Graph-Based Genome Alignment and Genotyping with HISAT2 and HISAT-genotype
# [2] Siren, J., Valimaki, N. & Makinen, V. Indexing Graphs for Path Queries with Applications in Genome Research. Ieee-Acm Transactions on Computational Biology and Bioinformatics 11, 375-388 (2014).

import sys

# Read a 6-bp genome sequence
refseq = ""
for line in open("small.fa"):
    if line.startswith('>'):
        continue
    line = line.strip()
    line = line.replace('N', '')
    refseq += line

# Print the genome sequence
print >> sys.stderr, "Reference sequence:", refseq


# Reads three variants (a single base substitute, a deletion of one base, and an insertion of one base)
snps = []
for line in open("small.snp"):
    line = line.strip()
    if not line:
        continue
    _, snpType, _, pos, data  = line.split()
    pos = int(pos) # position is zero-based (e.g., the first base position starts at number 0)

    snps.append([snpType, pos, data])

# Print SNPs (SNP is used here as a general term to represent small variants including small insertions and deletions)
print >> sys.stderr, "SNPs:"
for snpType, pos, data in snps:
    print >> sys.stderr, " ", snpType, pos, data
print >> sys.stderr


# Create a graph genome representation
class NODE:
    def __init__(self, pos_, label_):
        self.pos = pos_
        self.label = label_

class EDGE:
    def __init__(self, frm_, to_):
        self.frm = frm_
        self.to = to_
        
nodes = []
for nt in refseq:
    nodes.append(NODE(len(nodes), nt))
# Add a new node labeled 'Z' to the end of the graph
nodes.append(NODE(len(nodes), 'Z'))

edges = []
for i in range(len(nodes) - 1):
    edges.append(EDGE(i, i + 1))
# Add an edge from the 'Z' node to the first node of the graph
edges.append(EDGE(len(nodes) - 1, 0))

def addSNP(pos, snpType, data):
    assert pos > 0 # this implementation does not support a variant at the first base
    
    if snpType == "single":
        nodeID = len(nodes)
        nodes.append(NODE(pos, data))
        
        edges.append(EDGE(pos - 1, nodeID))
        edges.append(EDGE(nodeID, pos + 1))

    elif snpType == "deletion":
        delLen = int(data)
        edges.append(EDGE(pos - 1, pos + delLen))
        
    else:
        assert snpType == "insertion"
        nodeID = len(nodes)
        insLen = len(data)
        for i in range(insLen):
            nt = data[i]
            nodes.append(NODE(pos, nt))
        edges.append(EDGE(pos - 1, nodeID))
        edges.append(EDGE(len(nodes) - 1, pos))
        

for snpType, pos, data in snps:
    addSNP(pos, snpType, data)

# Print the graph genome representation in a user-friendly text format
def printGraph(refseq, nodes, edges):
    seqLen = len(refseq) + 1
    width = seqLen * 2 - 1

    head, output = "", ""
    for node in nodes[:seqLen]:
        head += ("%d " % node.pos)
        output += node.label
        if node.label != 'Z':
            output += " "

    print >> sys.stderr, head
    print >> sys.stderr, output
    print >> sys.stderr

    for i in range(seqLen, len(nodes)):
        node = nodes[i]
        print >> sys.stderr, "Node #%-2d: %c at %d" % (i, node.label, node.pos)
    
    for i in range(len(edges)):
        edge = edges[i]
        if edge.frm + 1 == edge.to:
            continue
        print >> sys.stderr, "Edge #%-2d: %d ---> %d" % (i, edge.frm, edge.to)
    print >> sys.stderr
    

# DK - work in progress
# Print the graph genome representation in a user-friendly diagram format
def drawGraph(refseq, nodes, edges):
    seqLen = len(refseq) + 1
    width = seqLen * 2 - 1

    lines = []
    head, output = "", ""
    for node in nodes[:seqLen]:
        head += ("%d " % node.pos)
        output += node.label
        if node.label != 'Z':
            output += " "
    lines.append(list(output))

    for edge in edges:
        fromPos, toPos = nodes[edge.frm].pos, nodes[edge.to].pos
        fromX, toX = fromPos * 2, toPos * 2

        print fromPos, "->", toPos
        print fromX, toX

        found = False
        for l in range(len(lines)):
            line = lines[l]
            empty = True
            for c in range(fromX + 1, toX ):
                if line[c] != " ":
                    empty = False
                    break
            if empty:
                for c in range(fromX + 1, toX):
                    line[c] = "-"
                lines[l] = line
                found = True
                break

        if not found:
            line = [" "] * (seqLen * 2 - 1)
            for c in range(fromX + 1, toX):
                line[c] = "-"
            lines.append(line)
            

    print >> sys.stderr, head
    for line in lines:
        line = ''.join(line)
        print >> sys.stderr, line


printGraph(refseq, nodes, edges)
# drawGraph(refseq, nodes, edges)

# Note that this implementation does not include a reverse determinization routine,
# which is not needed for the small example genome sequence.
# TODO: reverse determinization algorithm (C++ implementation is available in gbwt_graph.h in the HISAT2 source code)

# 1. Perform prefix-doubling sorting
class PATHNODE:
    def __init__(self, frm_, to_, key1_, key2_):
        self.frm = frm_
        self.to = to_
        self.key1 = key1_
        self.key2 = key2_

    def display(self):
        print "\t%d ==> %d (%d, %d)" % (self.frm, self.to, self.key1, self.key2)

class PATHEDGE:
    def __init__(self, frm_, to_, labelNum_):
        self.frm = frm_
        self.to = to_
        self.labelNum = labelNum_

# 1.1. Initialize path nodes (or paths)
label2num = {"A":0, "C":1, "G":2, "T":3, "Z":4}
paths = []
for edge in edges:
    node = nodes[edge.frm]
    path = PATHNODE(edge.frm, edge.to, label2num[node.label], 0)
    paths.append(path)

# 1.2. Sort paths
def pathSortID(a, b):
    if a.frm != b.frm:
        return a.frm - b.frm
    if a.to != b.to:
        return a.to - b.to
    if a.key1 != b.key1:
        return a.key1 - b.key1
    else:
        return a.key2 - b.key2

def pathSortKey(a, b):
    if a.key1 != b.key1:
        return a.key1 - b.key1
    if a.key2 != b.key2:
        return a_key2 - b_key2
    if a.frm != b.frm:
        return a.frm - b.frm
    return a.to - b.to

paths = sorted(paths, cmp=pathSortKey)

def assignRank(paths):
    if len(paths) <= 0:
        return

    prev_key = paths[0].key1
    prev_rank = 0
    paths[0].key1 = paths[0].key2 = 0

    for i in range(1, len(paths)):
        curr_key = paths[i].key1
        if prev_key == curr_key:
            paths[i-1].key1 = paths[i].key1 = prev_rank
            paths[i-1].key2 = paths[i].key2 = 1 # 1 means tie
            isSorted = False
        else:
            prev_key = curr_key
            paths[i].key1 = i
            paths[i].key2 = 0 # 0 means single?
            prev_rank = i

assignRank(paths)

def prune(paths):
    newPaths = []
    i = 0
    while i < len(paths):
        same = True
        path = paths[i]
        key = path.key1
        j = i + 1
        while j < len(paths):
            path2 = paths[j]
            key2 = path2.key1
            if key != key2:
                if not same:
                    break
                if path.frm != path2.frm:
                    break

                key = key2
                
            if path.frm != path2.frm:
                same = False
            j += 1

        if same:
            newPaths.append(paths[i])
        else:
            for k in range(i, j):
                newPaths.append(paths[k])            
        i = j

    return newPaths
    

def isSorted(paths):
    for i in range(len(paths)):
        path = paths[i]
        if path.key1 != i:
            return False
        
    return True

# 1.3. Elongate paths twofold (i.e., path doubling)

def binarySearch(paths, ID):
    l, r = 0, len(paths)
    while l < r:
        m = (l + r) / 2
        tmpID = paths[m].frm
        if tmpID == ID:
            while m > 0 and paths[m-1].frm == ID:
                m -= 1
            return m                
        elif tmpID > ID:
            r = m
        else:
            l = m + 1
            
    return -1

print >> sys.stderr, 0
for path in paths:
    path.display()

# Path doubling in an iterative way,
# e.g., iteration 1: path length is 2 (2^1)
#       iteration 2: path length is 4 (2^2)
#       ...
#       iteration n: path length is 2^n
iter = 1
while True:    
    paths = sorted(paths, cmp=pathSortID)
    MAXKEY = len(paths)
    
    newPaths = []
    for i in range(len(paths)):
        path = paths[i]
        if path.key2 == 0:
            newPath = PATHNODE(path.frm, path.to, path.key1 * MAXKEY, 0)
            newPaths.append(newPath)
            continue

        j = binarySearch(paths, path.to)
        for j in range(j, len(paths)):
            path2 = paths[j]
            if path.to < path2.frm:
                break

            newPath = PATHNODE(path.frm, path2.to, path.key1 * MAXKEY + path2.key1, 0)
            newPaths.append(newPath)

    paths = sorted(newPaths, cmp=pathSortKey)

    print >> sys.stderr, iter
    for path in paths:
        path.display()

    paths = prune(paths)
    assignRank(paths)

    print >> sys.stderr, iter
    for path in paths:
        path.display()

    if isSorted(paths):
        break    

    iter += 1
print >> sys.stderr


# 2. Create a prefix-sorted graph genome representation, which is equivalent to the above original graph representation
#    in terms of the language (a set of strings) that both graph representations define.
#    The prefixed-sorted form provides yet a better capability for search and storage.
paths = sorted(paths, cmp=pathSortID)
pathNodes = paths
pathEdges = []

# 2.1. Store genomic positions to pathNodes.to
#      ("to" variable is no longer needed at this stage and after, so this uses the space for storing a position)
for pathNode in pathNodes:
    pathNode.to = nodes[pathNode.frm].pos

# 2.2. Build an index for pathNodes using an unused field, key2
#      (like the above "to" variable, this uses the space for storing a position)
for i in range(len(pathNodes)):
    pathNode = pathNodes[i]
    pathNodes[pathNode.frm + 1].key2 = i + 1

# 2.3. Count the number of edges needed to construct the prefix-sorted graph
#      so that we can allocate the memory necessary for storing edges
labelIndex = [0] * len(label2num)
for edge in edges:
    label = nodes[edge.frm].label
    labelNum = label2num[label]
    edgeNum = pathNodes[edge.to + 1].key2 - pathNodes[edge.to].key2
    assert edgeNum > 0
    labelIndex[labelNum] += edgeNum

totEdges = 0
for i in range(len(labelIndex)):
    totEdges += labelIndex[i]
    labelIndex[i] = totEdges - labelIndex[i]

# 2.4. Create initial pathEdges
pathEdges = [[]] * totEdges
for edge in edges:
    label = nodes[edge.frm].label
    labelNum = label2num[label]
    from_i, to_i = pathNodes[edge.to].key2, pathNodes[edge.to+1].key2
    for i in range(from_i, to_i):
        pathNode = pathNodes[i]
        pathEdges[labelIndex[labelNum]] = PATHEDGE(edge.frm, pathNode.key1, labelNum)
        labelIndex[labelNum] += 1

# 2.5. Sort pathNodes and pathEdges
#      Sort pathNodes by rank
pathNodes = sorted(pathNodes, cmp=pathSortKey)
#      Sort pathEdges by label and then rank
def nodeEdge(a, b):
    if a.labelNum != b.labelNum:
        return a.labelNum - b.labelNum
    return a.to - b.to
pathEdges = sorted(pathEdges, cmp=nodeEdge)

print >> sys.stderr, "Nodes:"
print >> sys.stderr, " rank\tfrom"
for n in pathNodes:
    print >> sys.stderr, " %4d\t%4d" % (n.key1, n.frm)
print "Edges:"
print >> sys.stderr, " from\tto  base"
for e in pathEdges:
    print >> sys.stderr, " %4d\t%2d  %4c" % (e.frm, e.to, "ACGTZ"[e.labelNum])

# 2.6. Update pathEdges
#      Set PathNode.to = GraphNode.value and PathNode.key.first to outdegree                                                                                                                                                                
#      Replaces (from.from, to) with (from, to)
n, e = 0, 0
pathNodes[0].key1 = pathNodes[0].key2 = 0
while n < len(pathNodes) and e < len(pathEdges):
    node, edge = pathNodes[n], pathEdges[e]
    if node.frm == edge.frm:
        edge.frm = n
        e += 1
        node.key1 += 1
    else:
        n += 1
        if n < len(pathNodes):
            pathNodes[n].key1 = pathNodes[n].key2 = 0

print >> sys.stderr
print >> sys.stderr
print >> sys.stderr, "Nodes:"
print >> sys.stderr, " rank\tfrom\toutdegree"
for i in range(len(pathNodes)):
    n = pathNodes[i]
    print >> sys.stderr, " %4d\t%4d\t%9d" % (i, n.frm, n.key1)
print "Edges:"
print >> sys.stderr, " from\tto  base"
for e in pathEdges:
    print >> sys.stderr, " %4d\t%2d  %4c" % (e.frm, e.to , "ACGTZ"[e.labelNum])

    
# 3. Build a tabular representation for the prefix sorted graph constructed above
table = []
for e in range(len(pathEdges)):
    edge = pathEdges[e]
    label = "ACGTZ"[edge.labelNum]
    table.append([edge.frm, label])
pathEdges = sorted(pathEdges, cmp=lambda a, b: a.to - b.to)
incoming = {}
for e in range(len(pathEdges)):
    edge = pathEdges[e]
    label = "ACGTZ"[edge.labelNum]
    table[e].extend([label, edge.to])
    if edge.to not in incoming:
        incoming[edge.to] = e

def displayTable(table, range1 = None, range2 = None):
    for i in range(len(table)):
        rank, first, last, rank2 = table[i]
        output = "\t"
        if range1 and i in range1:
            output += "*"
        else:
            output += " "
        output += "%d  %c" % (rank + 1, first)
        output += "\t\t"
        output += "%c  %2d" % (last, rank2 + 1)
        if range2 and i in range2:
            output += "*"
        
        print >> sys.stderr, output

print >> sys.stderr
print >> sys.stderr, "Table:"
displayTable(table)


# 4. Perform alignment of a query, "TAG"
def align(table, incoming, seq):
    if len(seq) <= 0:
        return

    seq = seq[::-1]
    nt = seq[0]
    ntNum = label2num[nt]
    bs = labelIndex[ntNum-1] if ntNum > 0 else 0
    be = labelIndex[ntNum]
    ns, ne = table[bs][0], table[be][0]

    print >> sys.stderr
    print >> sys.stderr, nt
    displayTable(table, range(bs, be))

    for i in range(1, len(seq)):
        nt = seq[i]
        ntNum = label2num[nt]
        bs, be = incoming[ns], incoming[ne]

        print >> sys.stderr
        print >> sys.stderr, nt
        displayTable(table, None, range(bs, be))

        bs2, be2 = 0, 0
        for j in range(len(table)):
            nt_ = table[j][2]
            if nt == nt_:
                if j <= bs:
                    bs2 += 1
                if j <= be:
                    be2 += 1

        if ntNum > 0:
            bs2 += labelIndex[ntNum-1]
            be2 += labelIndex[ntNum-1]

        ns, ne = table[bs2][0], table[be2][0]

        print >> sys.stderr, "position:", pathNodes[ns].to
        displayTable(table, range(bs2, be2))
    

align(table, incoming, "TAG")
    
