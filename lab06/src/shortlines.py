import sys
import os

if len(sys.argv) < 3:
    print("사용법: python3 src/shortlines.py <FASTA파일> <최소길이>")
    sys.exit(1)

filename = sys.argv[1]
minlen = sys.argv[2]

if not minlen.isdigit():
    print("오류: 두 번째 인자가 숫자가 아닙니다:", minlen)
    sys.exit(1)

if not os.path.isfile(filename):
    print("오류: 파일을 찾을 수 없습니다:", filename)
    sys.exit(1)

minlen = int(minlen)
count = 0

with open(filename) as f:
    for line in f:
        line = line.rstrip()
        if not line.startswith(">"):
            if len(line) < minlen:
                count = count + 1

print("짧은 서열 줄 개수:", count)