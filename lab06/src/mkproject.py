import sys
import os

if len(sys.argv)<2:
    print("사용법: python3 src/mkproject.py <프로젝트이름>")
    sys.exit(1)

name=sys.argv[1]

if os.path.isdir(name):
    print("오류: 이미 존재하는 폴더입니다.")
    sys.exit(1)

os.makedirs(name + "/data")
os.makedirs(name + "/doc")
os.makedirs(name + "/src")

print(name, "폴더를 만들었습니다.")

