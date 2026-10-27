# lab07 요약 — 함수와 파일 저장

lab07에서는 반복되는 FASTA 처리 코드를 **함수**로 묶어 모듈(`fasta.py`)로 만들고, 다른 스크립트에서 `import`해 재사용하는 방법과 결과를 **파일로 저장**하는 방법을 익혔다.

## 1. 디렉터리 구성

| 폴더 | 내용 |
|------|------|
| `src/` | 파이썬 스크립트 (함수 모듈과 이를 사용하는 프로그램) |
| `data/` | 입력 FASTA 파일 (`seqs.fasta`, `seqs2.fasta`, `lower.fasta`) |
| `doc/` | 프로그램이 만든 출력 파일 (`long.fasta`, `summary.tsv`) |

## 2. 함수 기초

- **`fseqlen.py`** — `print`하는 함수와 `return`하는 함수의 차이.
  `length_print()`는 값을 돌려주지 않으므로 결과가 `None`이 되고, `length_return()`은 `4`를 돌려준다.
- **`fgc.py`** — `gc_content(seq)` 함수를 정의하고 호출하는 예. GC 비율 = (G 개수 + C 개수) / 서열 길이.

## 3. 함수 모듈 `fasta.py`

| 함수 | 역할 |
|------|------|
| `read_fasta(filename)` | FASTA 파일을 읽어 `{이름: 서열}` 딕셔너리로 반환. 헤더의 첫 단어만 이름으로 쓰고, 여러 줄 서열을 이어 붙이며 대문자로 변환 |
| `gc_content(seq)` | GC 비율(0~1) 반환. 빈 서열이면 `0.0` |
| `write_fasta(seqs, filename)` | 딕셔너리를 FASTA 파일로 저장 (`"w"` 모드, `out.write()`) |
| `reverse_complement(seqs)` | 상보 서열을 만든 뒤 역순으로 반환 (실습 중 작성) |

`if __name__ == "__main__":` 블록 덕분에 `python3 fasta.py data/seqs.fasta`처럼 직접 실행하면 이름·길이·GC를 출력하고, 다른 파일에서 `import`할 때는 실행되지 않는다.

## 4. 모듈을 사용하는 스크립트

| 스크립트 | 사용법 | 기능 |
|----------|--------|------|
| `seqlen2.py` | `python3 seqlen2.py <FASTA>` | 각 서열의 길이 출력 |
| `countseq2.py` | `python3 countseq2.py <FASTA>` | 서열 개수 출력, 인자 누락·파일 없음 오류 처리(`sys.exit`, `os.path.isfile`) |
| `filter.py` | `python3 filter.py <FASTA>` | 길이 20~40, GC 0.4~0.6 조건을 만족하는 서열 출력 |
| `filter_fasta.py` | `python3 filter_fasta.py <입력> <최소길이> <출력>` | 최소 길이 이상인 서열만 골라 새 FASTA로 저장 |
| `summary.py` | `python3 summary.py <입력> <출력.tsv>` | 서열별 이름·길이·GC를 탭 구분(TSV) 파일로 저장 |
| `test.py` | `python3 test.py` | `reverse_complement` 시험 호출 |

## 5. 실행 결과 (`data/seqs.fasta` 기준)

`summary.py` → `doc/summary.tsv`

```
name	length	gc
gene1	30	0.5
gene2	15	0.4667
gene3	22	0.5455
```

`filter_fasta.py` (최소 길이 20) → `doc/long.fasta`: 3개 중 `gene1`, `gene3` 2개 저장.

## 6. 핵심 정리

- `def`로 함수를 정의하고 `return`으로 값을 돌려준다. `print`만 하는 함수는 `None`을 반환한다.
- 공통 함수는 모듈 파일로 분리하고 `from fasta import read_fasta`처럼 가져와 재사용한다.
- `with open(파일, "w") as out:` + `out.write()`로 결과를 파일에 저장한다. 줄바꿈(`\n`)·탭(`\t`)은 직접 넣어야 한다.
- `sys.argv`로 입력·출력 파일 이름과 옵션을 명령행에서 받는다.

## 7. 남은 개선점

- `countseq2.py`: `read_fasta()`를 인자 검사보다 먼저 호출해 인자가 없으면 오류가 나고, 서열 개수를 두 번 출력한다.
- `filter.py`: `fasta.py`를 import하지 않고 같은 코드를 다시 작성했으며, 조건식 끝의 `<5`는 불필요하다.
- `reverse_complement()`: 문자열이 아닌 리스트를 반환하므로 `"".join(...)`이 필요하고, `test.py`는 결과를 출력하지 않는다.
