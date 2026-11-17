#!/usr/bin/env python3
"""길이 L 인 서열에서 만들 수 있는 k-mer 의 개수를 계산한다.

사용법: python3 count_kmers.py L k
"""
import sys


def count_kmers(L, k):
    """길이 L 인 서열에서 나오는 k-mer 의 개수(L - k + 1)를 돌려준다.

    - k > L 이면 길이 k 인 창(window)이 서열 안에 하나도 들어가지 않으므로 0 을 돌려준다.
    - L < 0 이거나 k <= 0 이면 의미 없는 입력이므로 ValueError 를 낸다.
    """
    if L < 0:
        raise ValueError(f"서열 길이 L 은 0 이상이어야 합니다: L={L}")
    if k <= 0:
        raise ValueError(f"k 는 1 이상이어야 합니다: k={k}")
    if k > L:
        return 0
    return L - k + 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python3 count_kmers.py L k", file=sys.stderr)
        sys.exit(1)
    L = int(sys.argv[1])
    k = int(sys.argv[2])
    print(f"L={L}, k={k} -> k-mer 개수: {count_kmers(L, k)}")
