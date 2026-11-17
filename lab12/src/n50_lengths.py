"""contig 길이 목록으로 N50 을 계산한다.

사용법:
    python3 n50_lengths.py 100 200 300 400      # 길이를 인자로 입력
    cat lengths.txt | python3 n50_lengths.py    # 표준입력으로 입력 (공백·줄바꿈 구분)
"""
import sys


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
    if len(sys.argv) > 1:
        words = sys.argv[1:]
    else:
        words = sys.stdin.read().split()

    lengths = []
    for word in words:
        if not word.isdigit() or int(word) == 0:
            sys.exit(f"오류: 양의 정수가 아닌 값이 있습니다: {word}")
        lengths.append(int(word))

    if not lengths:
        sys.exit("오류: contig 길이를 입력하세요.")

    print("contig 개수:", len(lengths))
    print("전체 길이:", sum(lengths))
    print("가장 긴 contig:", max(lengths))
    print("N50:", n50(lengths))
