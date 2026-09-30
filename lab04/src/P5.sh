#!/usr/bin/bash
FILE=$1
RESULT=$2

cat $FILE | tr -s " " "\n" | sort | uniq -c | sort -nr | head -10 > $RESULT