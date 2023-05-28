#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
fi

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit
fi


ticker=$1

rm -f results.txt; for i in `ls -1 *py | egrep -v BENCH`;do ( test -x $i && python3 $i -t $ticker | egrep Profit >> results.txt; echo >> results.txt);done

date > r.tmp

cat results.txt  | egrep -v gained | egrep '%' | sed s'/%//g' | awk '{ print $3 " "  $1 " " $6}' | sort -nr -k 3 >> r.tmp

mv -f r.tmp results.txt

git add . && git commit -m 'backtest results update' && git push

