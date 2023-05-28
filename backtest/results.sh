#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Try $0 <ticker>"
    exit
fi

if [ -z "$1" ]
  then
    echo "Try $0 <ticker>"
    exit
fi


ticker=$1
rm -f results.txt
rm -f results/$ticker.txt; for i in `ls -1 *py | egrep -v BENCH`;do (echo "Running python3 $i -t $ticker"; test -x $i && python3 $i -t $ticker | egrep Profit >> results.txt; echo >> results.txt);done

date > r.tmp

cat results.txt  | egrep -v gained | egrep '%' | sed s'/%//g' | awk '{ print $3 " "  $1 " " $6}' | sort -nr -k 3 >> r.tmp

mv -f r.tmp results/$ticker.txt 
rm -f results.txt

#git add . && git commit -m 'backtest results update' && git push

