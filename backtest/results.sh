#!/bin/bash

rm -f results.txt; for i in `ls -1 *py | egrep -v BENCH`;do ( sleep 3; test -x $i && python3 $i | egrep Profit >> results.txt; echo >> results.txt);done

date > r.tmp
cat results.txt  | egrep AAPL | egrep -v gained | sed s'/%//g' | awk '{ print "AAPL "  $1 " " $6}' | sort -nr -k 3 >> r.tmp
mv -f r.tmp results.txt

git add . && git commit -m 'backtest results update' && git push

