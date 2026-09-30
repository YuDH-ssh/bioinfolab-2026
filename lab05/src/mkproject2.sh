#!/usr/bin/bash
 
if [ -z "$1" ]
then
    echo "올바른 인자 입력해라"
    exit 1
fi 

if [ -d "$1" ]
then
    echo "오류"
    exit 1
fi

NAME=$1

mkdir $NAME
echo "$NAME 폴더를 만들었습니다"

tree $NAME