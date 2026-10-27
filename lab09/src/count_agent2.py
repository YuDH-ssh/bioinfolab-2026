#!/usr/bin/env python3
# count_agent2.py — FASTA 파일의 서열 개수를 출력한다 (lab07 fasta 모듈의 read_fasta 사용)
# 사용법: python3 count_agent2.py <FASTA파일>

import sys
import os

# lab07/src/fasta.py 를 import 할 수 있도록 경로를 추가한다
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab07", "src"))
from fasta import read_fasta

if len(sys.argv) < 2:
    print("사용법: python3 count_agent2.py <FASTA파일>")
    sys.exit(1)

filename = sys.argv[1]

if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(2)

seqs = read_fasta(filename)
print(len(seqs))
