#!/usr/bin/bash
 
NAME=$1
 
mkdir -p $NAME/data $NAME/doc $NAME/src
echo "프로젝트: $NAME" > $NAME/doc/README
echo "생성일: $(date)" >> $NAME/doc/README
 
echo "$NAME 프로젝트를 만들었습니다."
ls -R $NAME