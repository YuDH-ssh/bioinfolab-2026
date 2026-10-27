# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 저장소 개요

생물정보학실험 수업의 학생 실습 저장소이다. 빌드·린트·테스트 체계는 없고, 주차별 폴더(`labNN/`)에 셸 스크립트와 파이썬 스크립트를 쌓아 가는 구조다. 문서·주석·출력 메시지는 모두 한국어로 쓴다.

## 폴더 규칙

- 새 주차 폴더는 `cp -r lab-template labNN` 으로 만든다. 각 폴더는 `data/`(입력·생성 데이터), `doc/`(보고서·결과), `src/`(직접 작성한 `.sh`, `.py`)로 나뉜다.
- `resources/` 에는 수업에서 나눠 준 공용 예제 데이터(`resources/data/`)와 예제 스크립트(`resources/src/`)가 있다.
- `prob03/` 등 `probNN/` 은 과제 폴더다.
- 하위 폴더에 `CLAUDE.md` 가 있으면 그 폴더 작업 시 해당 규칙을 따른다 (예: `lab09/CLAUDE.md` — rm·pip install·git 명령 금지, 새 라이브러리 사용 전 확인).

## 코드 구조

- 주차가 진행되며 같은 작업(FASTA 서열 개수·길이·GC 비율 등)을 bash(lab04~05) → 파이썬(lab06) → 함수 모듈(lab07) 순으로 다시 구현한다.
- 공용 FASTA 모듈은 `lab07/src/fasta.py` 이다: `read_fasta`(헤더 첫 단어를 이름으로, 여러 줄 서열을 이어 붙이고 대문자화하여 `{이름: 서열}` 반환), `gc_content`, `write_fasta`, `reverse_complement`. 새 파이썬 코드에서 FASTA 를 읽을 때는 이 `read_fasta` 를 쓴다.
- 이 모듈을 쓰는 스크립트들은 `from fasta import ...` 로 같은 폴더에서 import 하므로, `src/` 에 있는 스크립트를 기준으로 실행한다.
- 외부 라이브러리(Biopython 등) 없이 표준 라이브러리만 쓴다.

## 실행

스크립트는 인자로 파일 경로를 받아 직접 실행한다. 예:

```
python3 lab07/src/fasta.py lab07/data/seqs.fasta          # 이름 길이 GC 출력
python3 lab07/src/summary.py lab07/data/seqs.fasta lab07/doc/summary.tsv
bash lab05/src/fastainfo.sh lab05/data/seqs.fasta
```

## 실행 환경

- Codespaces devcontainer 가 4종 있다 (`.devcontainer/1-basic`, `2-conda`, `3-seq`, `4-genome`). 주차에 따라 사용 가능한 도구가 다르다: 기본(python3), conda(micromamba), 서열 분석(seqkit, blastn, mafft, iqtree, fastqc, fastp), 유전체(+ shovill, prokka).
- 현재 환경에 어떤 도구가 있는지는 `bash .devcontainer/check.sh` 로 확인한다.
- `$MYHOME` 은 저장소 루트를 가리킨다.
- FASTQ/SRA 등 시퀀싱 원자료와 조립·주석 결과 폴더(shovill/spades/prokka/flye), FastQC 보고서는 `.gitignore` 로 제외된다 — 필요하면 wget 으로 다시 내려받는다.
