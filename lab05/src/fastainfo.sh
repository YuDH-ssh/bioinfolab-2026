#파일 이름 인자로 입력 받기
FILE="$1"

#파일 이름 출력
echo "파일:" "$1"

#서열 개수 출력
N=$(grep -c ">" "$1")
echo "서열 갯수: $N"

#서열 이름 목록 (꺽쇠 없이 첫 단어만) 출력
echo "서열 이름:"
grep ">" "$FILE" | cut -d " " -f1 | tr -d ">" 

#grep으로 헤더줄만 뽑고 cut, tr로 다듬기 
#(4번 수업의 과정 5번 참고. 
#grep -v (헤더 빼기), tr -d (줄바꿈 삭제)

#헤더를 뺀 줄의 총 글자 출력
TOTAL=$(grep -v ">" "$FILE" | tr -d "\n" | wc -c)
echo "총 염기 수(대략): $TOTAL"