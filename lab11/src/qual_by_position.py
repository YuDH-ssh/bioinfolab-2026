import sys

# 사용법: python3 qual_by_position.py <FASTQ 파일>
# 모든 read 에서 같은 위치(1번째, 2번째, ... 염기)의 품질 점수를 모아
# 위치별 평균 품질을 "위치<TAB>평균품질" 형식으로 출력한다.
# 품질 점수는 Phred+33 인코딩(점수 = ord(문자) - 33)으로 계산한다.


def read_fastq(filename):
    """FASTQ 파일을 읽어 (이름, 서열, 품질) 튜플의 리스트를 돌려준다."""
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


def quality_by_position(reads):
    """위치별 품질 점수 합계와 개수를 모아 위치별 평균 리스트를 돌려준다.

    read 길이가 서로 달라도 되도록, 각 위치마다 그 위치까지 있는
    read 의 개수로 나눈다.
    """
    sums = []    # sums[i]   : i번째 위치 품질 점수의 합
    counts = []  # counts[i] : i번째 위치에 염기가 있는 read 수
    for name, seq, qual in reads:
        for i, ch in enumerate(qual):
            score = ord(ch) - 33
            if i >= len(sums):
                sums.append(0)
                counts.append(0)
            sums[i] = sums[i] + score
            counts[i] = counts[i] + 1

    means = []
    for i in range(len(sums)):
        means.append(sums[i] / counts[i])
    return means


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용법: python3 qual_by_position.py <FASTQ 파일>", file=sys.stderr)
        sys.exit(1)

    reads = read_fastq(sys.argv[1])
    means = quality_by_position(reads)

    for i, m in enumerate(means):
        print(f"{i + 1}\t{m:.2f}")
