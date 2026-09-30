#!/usr/bin/bash
 
for F in data/*.fasta
do
    N=$(grep -c ">" $F)
    echo "$F 파일에는 서열이 $N 개 있습니다."
done