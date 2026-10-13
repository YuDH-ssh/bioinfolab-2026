import sys
from fasta import read_fasta
 
seqs = read_fasta(sys.argv[1])

for i in seqs:
    print(len(seqs[i]))