#폴더 이름을 인자로 받아 파일명과 서열 갯수를 출력하는 스크립트

if [ -z "$1" ]
then
    echo "사용법: $0 <폴더>"
    exit 1
fi 

FOLDER=$1

if [ ! -d "$1" ]
then
    echo "폴더 미존재"
    exit 1
fi

echo -e "file\tcount"

for F in "$1"/*.fasta
do
    if [ ! -f "$F" ]
    then
        echo "오류"
        exit 1
    fi

    N=$(grep -c ">" "$F")
    echo -e "$F\t$N"
done