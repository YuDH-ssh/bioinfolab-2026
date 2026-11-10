import sys
import random

# 사용법: python3 gc_content.py <FASTQ 파일> [고를 read 수(기본 10)]
#
# 1) 각 read 의 GC 비율(G+C 개수 / 서열 길이)과 평균 품질을 계산한다.
#    품질 점수는 Phred+33 인코딩(점수 = ord(문자) - 33)으로 계산한다.
# 2) GC 비율이 전체 평균 GC 비율에서 가장 많이 벗어난(극단적으로 높거나 낮은)
#    read 를 N개(기본 10개) 고른다.
# 3) 고른 read 들의 평균 품질을 전체 read 평균 품질과 비교한다.
#    차이가 우연인지 보기 위해, 전체 read 에서 무작위로 N개씩 뽑아
#    평균 품질을 구하는 일을 여러 번 반복하는 순열(무작위 추출) 검정을 한다.


def read_fastq(filename):
    """FASTQ 파일을 읽어 (이름, 서열, 품질) 튜플의 리스트를 돌려준다."""
    records = []
    with open(filename) as f:
        lines = f.readlines()
    for i in range(0, len(lines), 4):
        name = lines[i].rstrip()[1:].split()[0]
        seq = lines[i + 1].rstrip()
        qual = lines[i + 3].rstrip()
        records.append((name, seq, qual))
    return records


def gc_ratio(seq):
    """서열의 GC 비율(0~1)을 돌려준다. 대소문자를 모두 센다."""
    gc = 0
    for base in seq:
        if base in "GCgc":
            gc = gc + 1
    return gc / len(seq)


def mean_quality(qual):
    """품질 문자열의 평균 Phred 점수를 돌려준다."""
    total = 0
    for ch in qual:
        total = total + (ord(ch) - 33)
    return total / len(qual)


def mean(values):
    return sum(values) / len(values)


def stdev(values):
    """표본 표준편차"""
    m = mean(values)
    total = 0
    for v in values:
        total = total + (v - m) ** 2
    return (total / (len(values) - 1)) ** 0.5


def read_stats(reads):
    """각 read 의 (이름, 길이, GC 비율, 평균 품질) 리스트를 돌려준다.

    길이가 0인 read(트리밍으로 서열이 모두 잘린 경우)는 건너뛴다.
    """
    stats = []
    for name, seq, qual in reads:
        if len(seq) == 0:
            continue
        stats.append((name, len(seq), gc_ratio(seq), mean_quality(qual)))
    return stats


def pick_extremes(stats, n):
    """GC 비율이 전체 평균에서 가장 많이 벗어난 read n개를 고른다."""
    gc_mean = mean([s[2] for s in stats])
    ranked = sorted(stats, key=lambda s: abs(s[2] - gc_mean), reverse=True)
    return ranked[:n]


def permutation_test(qualities, n, observed_diff, trials=10000, seed=1):
    """무작위로 n개 read 를 뽑았을 때 평균 품질 차이가
    관찰값만큼(절댓값 기준) 이상 벌어지는 비율(양측 p값)을 돌려준다."""
    random.seed(seed)  # 실행할 때마다 같은 결과가 나오도록 고정
    overall = mean(qualities)
    count = 0
    for _ in range(trials):
        sample = random.sample(qualities, n)
        if abs(mean(sample) - overall) >= abs(observed_diff):
            count = count + 1
    return (count + 1) / (trials + 1)


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("사용법: python3 gc_content.py <FASTQ 파일> [고를 read 수(기본 10)]",
              file=sys.stderr)
        sys.exit(1)

    n = 10
    if len(sys.argv) == 3:
        n = int(sys.argv[2])

    stats = read_stats(read_fastq(sys.argv[1]))
    if len(stats) <= n:
        print(f"read 수({len(stats)})가 고를 개수({n})보다 많아야 합니다.",
              file=sys.stderr)
        sys.exit(1)

    gcs = [s[2] for s in stats]
    quals = [s[3] for s in stats]
    gc_mean = mean(gcs)
    q_mean = mean(quals)
    q_sd = stdev(quals)

    print("# 전체 read")
    print(f"read 수\t{len(stats)}")
    print(f"평균 GC 비율\t{gc_mean:.4f}")
    print(f"평균 품질\t{q_mean:.2f}")
    print(f"품질 표준편차\t{q_sd:.2f}")
    print()

    extremes = pick_extremes(stats, n)
    print(f"# GC 비율이 극단적인 read {n}개 (평균 GC 에서 벗어난 정도 순)")
    print("이름\t길이\tGC비율\t구분\t평균품질")
    for name, length, gc, q in extremes:
        side = "높음" if gc > gc_mean else "낮음"
        print(f"{name}\t{length}\t{gc:.4f}\t{side}\t{q:.2f}")
    print()

    ext_quals = [s[3] for s in extremes]
    ext_mean = mean(ext_quals)
    diff = ext_mean - q_mean
    p = permutation_test(quals, n, diff)

    print("# 평균 품질 비교")
    print(f"극단 GC read 평균 품질\t{ext_mean:.2f}")
    print(f"전체 read 평균 품질\t{q_mean:.2f}")
    print(f"차이(극단 - 전체)\t{diff:+.2f}")
    print(f"순열 검정 p값(10000회)\t{p:.4f}")
    if p < 0.05:
        print("결론\t극단 GC read 의 평균 품질은 전체 평균과 유의하게 다르다 (p < 0.05).")
    else:
        print("결론\t극단 GC read 의 평균 품질은 전체 평균과 유의한 차이가 없다 (p >= 0.05).")
