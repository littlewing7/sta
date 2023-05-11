#!/bin/bash

ticker=$1

rm -f results.txt; for i in `ls -1 *py | egrep -v BENCH`;do ( sleep 3; test -x $i && python3 $i $ticker | egrep Profit >> results.txt; echo >> results.txt);done

date > r.tmp
cat results.txt  | egrep -v gained | egrep '%' | sed s'/%//g' | awk '{ print $3 " "  $1 " " $6}' | sort -nr -k 3 >> r.tmp
mv -f r.tmp results.txt

git add . && git commit -m 'backtest results update' && git push

