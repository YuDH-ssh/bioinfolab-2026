import sys

# 사용법: python3 check_paired.py <FASTQ 파일 1> <FASTQ 파일 2>
# paired-end FASTQ 두 파일이 올바르게 짝을 이루는지 확인한다.
#   1) 두 파일의 read 개수가 같은지
#   2) 같은 순서(같은 번째)에 있는 read 끼리 이름이 짝을 이루는지
# 이름은 헤더의 첫 단어(공백 앞)를 쓴다. 두 이름이 완전히 같으면 짝으로 보고,
# 다르면 끝의 짝 표시(기호 + 1/2, 예: /1 과 /2, .1 과 .2, _1 과 _2)를
# 떼어 낸 뒤 앞부분이 같은지 비교한다.


def read_names(filename):
    """FASTQ 파일을 읽어 각 read 이름(헤더 첫 단어)의 리스트를 돌려준다."""
    names = []
    with open(filename) as f:
        for i, line in enumerate(f):
            if i % 4 == 0:              # 4줄 중 첫 줄이 헤더(@이름 ...)
                name = line.rstrip()[1:].split()[0]
                names.append(name)
    return names


def is_pair(name1, name2):
    """두 read 이름이 짝을 이루면 True 를 돌려준다.

    - 두 이름이 완전히 같으면 짝 (예: SRR1553607.5 과 SRR1553607.5)
    - 아니면 name1 끝이 '기호+1', name2 끝이 '기호+2' 이고
      그 앞부분이 같으면 짝 (예: read123/1 과 read123/2)
    끝의 숫자를 아무거나 떼면 SRR1553607.5 와 SRR1553607.6 처럼
    서로 다른 read 도 같은 이름이 되므로, 짝 표시 1/2 만 인정한다.
    """
    if name1 == name2:
        return True
    if len(name1) < 3 or len(name2) < 3:
        return False
    if name1[-1] != "1" or name2[-1] != "2":
        return False
    if name1[-2].isalnum() or name2[-2].isalnum():   # 숫자 앞은 기호여야 함
        return False
    return name1[:-1] == name2[:-1]                  # 기호와 앞부분이 같아야 함


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("사용법: python3 check_paired.py <FASTQ 파일 1> <FASTQ 파일 2>", file=sys.stderr)
        sys.exit(1)

    names1 = read_names(sys.argv[1])
    names2 = read_names(sys.argv[2])

    # 1) read 개수 비교
    print("파일 1 read 개수:", len(names1))
    print("파일 2 read 개수:", len(names2))
    if len(names1) == len(names2):
        print("read 개수: 같음")
    else:
        print("read 개수: 다름")

    # 2) 같은 순서의 read 이름 비교 (개수가 다르면 짧은 쪽 길이까지만)
    mismatch = 0
    for i in range(min(len(names1), len(names2))):
        if not is_pair(names1[i], names2[i]):
            if mismatch < 10:           # 처음 10개만 자세히 출력
                print(f"짝 불일치: {i + 1}번째 read\t{names1[i]}\t{names2[i]}")
            mismatch = mismatch + 1

    print("이름이 짝을 이루지 않는 read 수:", mismatch)

    if len(names1) == len(names2) and mismatch == 0:
        print("결과: 두 파일은 올바른 paired-end 쌍입니다.")
    else:
        print("결과: 두 파일은 올바른 쌍이 아닙니다.")
