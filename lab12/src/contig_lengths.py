"""n50.py 확장: 조립 결과의 contig 길이를 내림차순으로 정렬해 파일에 한 줄씩 저장한다.

사용법:
    python3 contig_lengths.py <contigs.fa> [출력파일]
    (출력파일을 생략하면 doc/contig_lengths.txt 에 저장)
"""
import os
import sys

# 공용 FASTA 모듈(lab07/src/fasta.py)의 read_fasta 를 사용한다.
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "lab07", "src"))
from fasta import read_fasta


def n50(lengths):
    """길이를 내림차순으로 더해 가다 전체 길이의 절반 이상이 되는 contig 의 길이를 돌려준다."""
    lengths = sorted(lengths, reverse=True)
    half = sum(lengths) / 2

    running = 0
    for length in lengths:
        running = running + length
        if running >= half:
            return length


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("사용법: python3 contig_lengths.py <contigs.fa> [출력파일]")

    if len(sys.argv) > 2:
        outfile = sys.argv[2]
    else:
        outfile = "doc/contig_lengths.txt"

    seqs = read_fasta(sys.argv[1])
    lengths = []
    for name in seqs:
        lengths.append(len(seqs[name]))

    if not lengths:
        sys.exit("오류: FASTA 파일에 서열이 없습니다.")

    lengths = sorted(lengths, reverse=True)

    with open(outfile, "w") as out:
        for length in lengths:
            out.write(str(length) + "\n")

    print("contig 개수:", len(lengths))
    print("전체 길이:", sum(lengths))
    print("가장 긴 contig:", max(lengths))
    print("N50:", n50(lengths))
    print("contig 길이를 저장했습니다:", outfile)
