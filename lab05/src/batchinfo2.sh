#딕셔너리 기능 보유
echo "" > count.txt

if [ -z "$1" ]
then
    echo "사용법: $0 <폴더>"
    exit 1
fi 

FOLDER=$1

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
    echo "$F $N" >> count.txt
done

echo ""
grep "$2" count.txt